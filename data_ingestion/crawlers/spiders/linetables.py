# -*- coding: utf-8 -*-
import sys
sys.path.append(r'\Coding Projects\matchup-analyzer\data_ingestion\dao')
import scrapy
from bs4 import BeautifulSoup as bs
import numpy as np
import datetime
import odds_dao

class LinetablesSpider(scrapy.Spider):
    name = 'parse_linetables'
    allowed_domains = ['www.vegasinsider.com/']

    def __init__(self, sport_name, vendor_id=1, earliest_event_date_epoch_ms=0, html_tag='tbody', class_dict={}, parser='lxml'):
        '''Takes a sport, vendor_id, earliest_even_date_epoc_ms, optional html_tag, class_dict and parser, 
        Gets all urls from the line_url_scheduling table for the given vendor_id and sport_id, where the
        event date is null or greater than the given earliest_event_date_epoch_ms and returns parsed table as game_data object
        :param earliest_event_date_epoch_ms: urls after this date will be retreived
        :param sport_id: sport_id
        :param game_time: the time the game starts/ed
        :param line_dict: dictionary of {sportsbook:array of line movement data}
        '''  
        self.earliest_event_date_epoch_ms = earliest_event_date_epoch_ms
        self.sport_id = odds_dao.get_sport_id_for_vendor(vendor_id, sport_name)
        self.vendor_id = vendor_id
        self.html_parser = HtmlParser(html_tag, class_dict, parser)

    def start_requests(self):
        line_urls = odds_dao.get_line_urls(self.vendor_id, self.sport_id, self.earliest_event_date_epoch_ms)

        for url in line_urls:
            yield scrapy.Request(url=url.url, callback=self.parse)

    def parse(self, response):
        game_data = self.html_parser.get_tables(response.body)
        yield {'game_data':game_data, 'sport_id': self.sport_id, 'vendor_id': self.vendor_id}


class SoupFactory(object):
    """Accepts html and outputs soup"""

    def __init__(self, parser):
        self.parser = parser

    def get(self, raw_html):
        return bs(raw_html, self.parser)


class HtmlParser(object):
    """Parses html soup for html_tag and optional class:value dict"""

    def __init__(self, html_tag, class_dict, parser):
        self.html_tag = html_tag
        self.class_dict = class_dict
        self.soup_factory = SoupFactory(parser)

    def get_tables(self, raw_html):
        """Takes raw_html from line movement pages, strips all data from table and returns gamedata object"""
        soup = self.soup_factory.get(raw_html)
        find_tables = soup.find_all(self.html_tag, self.class_dict)
        table_list = []

        for table in find_tables:
            if is_deepest_table(table, self.html_tag, self.class_dict):
                table_data = []
                rows = table.find_all('tr')

                for row in rows:
                    cols = row.find_all('td')
                    table_data.append([ele.get_text(strip=True) for ele in cols])

                table_list.append(table_data)

        return to_game_data(table_list)

def is_deepest_table(table_soup, html_tag, class_dict): 
    """Returns True if no child tables exist"""
    if len(table_soup.find_all(html_tag, class_dict)) == 0:
        return True
    return False


def to_game_data(table_list):
    """Extracts game data from table and returns GameData object"""
    teams = table_list[0][0][0].split(' @ ')
    away_team = teams[0]
    home_team = teams[-1]
    game_time = table_list[1][1][0][10:]
    string_date = table_list[1][0][0][10:]
    game_date = datetime.datetime.strptime(string_date, "%A, %B %d, %Y").strftime("%m-%d-%Y")
    return GameData(home_team, away_team, game_time, game_date, create_dict(table_list))

class GameData(object):
    """"GameData object with a dictionary of arrays for each sportsbooks line movement data
    :param home_team: the home team
    :param away_team: the away team
    :param game_time: the time the game starts/ed
    :param line_dict: dictionary of {sportsbook:array of line movement data}
    """
    def __init__(self, home_team, away_team, game_time, game_date, line_dict):
        self.home_team = home_team
        self.away_team = away_team
        self.game_time = game_time
        self.game_date = game_date
        self.line_dict = line_dict

def create_dict(table_list):
    """Creates dictionary 'Sportsbook name':array of line movements"""
    line_dict = {}
    for table in table_list[2:]:
        if len(table[0]) == 1:
            sportsbook_name = table[0][0][:-15].strip()
        line_dict[sportsbook_name] = np.array(table[2:])
    return line_dict