# -*- coding: utf-8 -*-
import sys
import scrapy
from bs4 import BeautifulSoup as bs
import numpy as np
import datetime as dt
import pytz
import re
from data_ingestion.dao import odds_dao

class VILinetablesSpider(scrapy.Spider):
    name = 'parse_line_tables'
    allowed_domains = ['www.vegasinsider.com/']

    def __init__(self, sport=None, vendor_id=1, earliest_event_date_epoch_ms=0, html_tag='tbody', class_dict={}, parser='lxml'):
        '''Takes a sport, vendor_id, earliest_even_date_epoc_ms, optional html_tag, class_dict and parser,
        Gets all urls from the line_url_scheduling table for the given vendor_id and sport_id, where the
        event date is null or greater than the given earliest_event_date_epoch_ms and returns parsed table as game_data object
        :param earliest_event_date_epoch_ms: urls after this date will be retreived
        :param sport: sport name string of urls to parse, if None will parse all urls in scheduling table
        :param html_tag: the html_tag to taget for table parsing, 'tbody' default for vegasinsider line movement pages
        :param class_dict: dictionary of css class:value to target for table parsing, default none for vegasinsider live movement pages
        :param parser: parser to use for html parsing, lxml default
        '''
        self.earliest_event_date_epoch_ms = earliest_event_date_epoch_ms
        self.sport_id = odds_dao.get_sport_id_for_vendor(vendor_id, sport) if sport is not None else None
        self.vendor_id = vendor_id
        self.html_parser = HtmlParser(html_tag, class_dict, parser)

    def start_requests(self):
        line_urls = odds_dao.get_line_urls(self.vendor_id, self.sport_id, self.earliest_event_date_epoch_ms)
        for line_url in line_urls:
            yield scrapy.Request(url=line_url.url, callback=self.parse, meta={'line_url':line_url})

    def parse(self, response):
        game_data = self.html_parser.get_tables(response.body)
        sport_id = response.request.meta['line_url'].sport_id
        yield {'game_data':game_data, 'sport_id': sport_id, 'vendor_id': self.vendor_id, 'url': response.request.url}


class SoupFactory(object):
    """Creates a soup factory object based on the parser chosen, get returns html soup via beautifulsoup"""

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
    away_team, home_team = table_list[0][0][0].split(' @ ')
    game_time_str = table_list[1][1][0][10:]
    game_date_str = table_list[1][0][0][10:]
    naive_game_time = dt.datetime.strptime(game_time_str, "%I:%M %p").time()
    game_date = dt.datetime.strptime(game_date_str, "%A, %B %d, %Y")
    tz = pytz.timezone('US/Eastern')
    game_naive_datetime = dt.datetime(game_date.year,
                                      game_date.month,
                                      game_date.day,
                                      naive_game_time.hour,
                                      naive_game_time.minute)
    game_datetime = tz.localize(game_naive_datetime)
    game_timestamp_ms = game_datetime.timestamp() * 1000
    line_dict = convert_line_times_to_timestamps(create_dict(table_list), game_datetime)
    return GameData(home_team, away_team, game_datetime, game_timestamp_ms, line_dict)

class Odds(object):

    def __init__(self, type, team_symbol, odds, spread=None, total=None):
        self.type = type
        self.team_symbol = team_symbol
        self.odds = odds
        self.spread = spread
        self.total = total

money_line_regx = re.compile(r'^([A-Z]{3})\s?([\+\-]\d+|XX)$')
spread_regx     = re.compile(r'^([A-Z]{3})(PK|XX|[\+\-]?\d+\.?\d?)\s*(XX|[\-\+]\d+)$')
total_regx = re.compile(r'^(\d+\.?\d|XX)\s*([\-\+]\d+|XX)$')
half_regx       = re.compile(r'^([A-Z]{3})(PK|XX|[\+\-]\d+\.?\d?)$')

def convert_bet_table_to_bet_objects(line_dict):
    """Uses an optional Line type or regex match to convert a line item string into a
    LineOdds object, or returns string if no match is found"""

    odds_dict = {}

    for sportsbook, bet_table in line_dict.items():
        odds_table = []
        for row in bet_table:
            snapshot_timestamp = row[0]
            fav_money_line = convert_string_bet_to_bet_object(row[2], "money_line")
            dog_money_line = convert_string_bet_to_bet_object(row[3], "money_line")
            fav_spread = convert_string_bet_to_bet_object(row[4], "spread")
            dog_spread = convert_string_bet_to_bet_object(row[5], "spread")
            fav_total = convert_string_bet_to_bet_object(row[6], "total")
            dog_total = convert_string_bet_to_bet_object(row[7], "total")
            fav_fst_half = convert_string_bet_to_bet_object(row[8], "half")
            dog_fst_half = convert_string_bet_to_bet_object(row[9], "half")
            fav_snd_half = convert_string_bet_to_bet_object(row[10], "half")
            dog_snd_half = convert_string_bet_to_bet_object(row[11], "half")
            odds_dict[sportsbook] = odds_table

def convert_string_bet_to_bet_object(string, type=None):
    if type == "money_line" or re.search(money_line_regx, string):
        team_symbol, odds = re.findall(money_line_regx, string)[0]
        type = "money_line"

        if odds == 'XX':
            odds = None
        return type, team_symbol, odds

    elif type == "spread" or re.search(spread_regx, string):
        team_symbol, spread, odds = re.findall(spread_regx, string)[0]
        type = "spread"
        if spread == 'XX' or odds == 'XX':
            spread, odds = None, None
        if spread == 'PK':
            spread = 0
        return type, team_symbol, odds, spread

    elif type == "total" or re.search(total_regx, string):
        total, odds = re.findall(total_regx, string)[0]
        type = "total"

        if total == 'XX' or odds == 'XX':
            odds, over_under = None, None
        return type, None, odds, total

    elif type == "half" or re.search(half_regx, string):
        team_symbol, odds = re.findall(half_regx, string)[0]
        type = "half"

        if odds == 'XX':
            odds = None
        if odds == 'PK':
            odds = 0
        return type, team_symbol, odds

    elif string == '':
        return None
    return string

class GameData(object):
    """"GameData object with a dictionary of arrays for each sportsbooks line movement data
    :param home_team: the home team
    :param away_team: the away team
    :param game_time: the time the game starts/ed
    :param line_dict: dictionary of {sportsbook:array of line movement data}
    """
    def __init__(self, home_team, away_team, game_datetime, game_timestamp_ms, line_dict):
        self.home_team = home_team
        self.away_team = away_team
        self.game_datetime = game_datetime
        self.game_timestamp = game_timestamp_ms
        self.line_dict = line_dict

def convert_line_times_to_timestamps(line_dict, game_datetime):
    line_snapshot_year = game_datetime.year
    tz = pytz.timezone('US/Eastern')
    for sportsbook_name, line_table in line_dict.items():
        for line in line_table:
            line_snapshot_month_str, line_snapshot_day_str = line[0].split(r"/")
            line_snapshot_time_str = line[1]
            line_snapshot_time = dt.datetime.strptime(line_snapshot_time_str, "%I:%M%p").time()
            line_snapshot_datetime = dt.datetime(line_snapshot_year,
                                                 int(line_snapshot_month_str),
                                                 int(line_snapshot_day_str),
                                                 line_snapshot_time.hour,
                                                 line_snapshot_time.minute)
            tz.localize(line_snapshot_datetime)
            line[0] = line_snapshot_datetime.timestamp() * 1000 #Convert to ms
    return line_dict

def create_dict(table_list):
    """Creates dictionary {'Sportsbook name':array of line movements}
    removes headers from table.
    """
    line_dict = {}
    for table in table_list[2:]:
        if len(table[0]) == 1:
            sportsbook_name = table[0][0][:-15].strip()
        line_table = np.array(table[2:])
        line_dict[sportsbook_name] = line_table
    return line_dict
