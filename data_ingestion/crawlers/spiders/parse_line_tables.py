# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup as bs
import datetime as dt
import pytz
import re
from data_ingestion.dao import odds_store, odds_entities

class VILinetablesSpider(scrapy.Spider):
    name = 'parse_line_tables'
    allowed_domains = ['www.vegasinsider.com/']

    def __init__(self, sport=None, vendor_id=1, earliest_event_date_epoch_ms=0):
        '''Takes a sport, vendor_id, earliest_even_date_epoc_ms, optional html_tag, class_dict and parser,
        Gets all urls from the line_url_scheduling table for the given vendor_id and sport_id, where the
        event date is null or greater than the given earliest_event_date_epoch_ms and returns parsed table as game_data object
        :param earliest_event_date_epoch_ms: urls after this date will be retreived
        :param sport: sport name string of urls to parse, if None will parse all urls in scheduling table
        '''
        self.earliest_event_date_epoch_ms = earliest_event_date_epoch_ms
        self.sport_id = odds_store.get_sport_id_for_vendor(vendor_id, sport) if sport is not None else None
        self.vendor_id = vendor_id
        self.game_data_factory = GameDataFactory(self.sport_id, self.vendor_id, html_parser='lxml')

    def start_requests(self):
        line_urls = odds_store.get_line_urls(self.vendor_id, self.sport_id, self.earliest_event_date_epoch_ms)
        for line_url in line_urls:
            yield scrapy.Request(url=line_url.url, callback=self.parse, meta={'line_url':line_url})

    def parse(self, response):
        game_data = self.game_data_factory(response.body, sport_id, vendor_id)
        sport_id = response.request.meta['line_url'].sport_id
        yield {'game_data':game_data, 'url': response.request.url}

class GameData(object):
    """"GameData object with a dictionary of arrays for each sportsbooks line movement data
    :param home_team: the home team
    :param away_team: the away team
    :param game_time: the time the game starts/ed
    :param line_dict: dictionary of {sportsbook:array of line movement data}
    """
    def __init__(self, sport_id, vendor_id, home_team, away_team, game_timestamp_ms, odds_list):
        self.sport_id = sport_id
        self.vendor_id = vendor_id
        self.home_team = home_team
        self.away_team = away_team
        self.game_timestamp = game_timestamp_ms
        self.odds_list = odds_list

class GameDataFactory(object):
    """Orchestrates the construction of a game data object from the raw html response of the scrapy spider"""

    def __init__(self, sport_id, vendor_id, html_parser='lxml'):
        self.sport_id = sport_id
        self.vendor_id = vendor_id
        self.line_table_parser = LineTableParser(parser=html_parser)
        self.row_count = 0

    def build_game_data(self, html_bytes):
        table_list = self.line_table_parser.get_tables(html_bytes)                   #Parse tables from raw html bytecode
        home_team, away_team, game_timestamp_ms, game_datetime_obj = extract_game_meta_data(table_list) #Get game meta data
        game_odds_list = self.convert_odds_table_to_odds_object_list(table_list, game_datetime_obj)          #Convert table strings to odds objects, insert into OddsUpdateBuilder                              #Build odds list
        return GameData(self.sport_id, self.vendor_id, home_team, away_team, game_timestamp_ms, game_odds_list)

    def convert_odds_table_to_odds_object_list(self, table_list, game_datetime_obj):
        """Takes an array of tables and strips data from each row,
            passes sportsbook name and row data (timestamp, odds offerings) to
            OddsUpdateBuilder, returns the built odds_list"""
        odds_list = []
        odds_update_builder = odds_entities.OddsUpdateBuilder()
        for table in table_list:
            if len(table[0]) == 1:
                sportsbook_name = table[0][0][:-15].strip()
            line_table = table[2:]
            for odds_row in line_table:
                snapshot_timestamp, list_of_odds = self.convert_odds_row_to_odds_objects(odds_row, sportsbook_name, game_datetime_obj)
                for odds_object in list_of_odds:
                    if odds_object is not None:
                        odds_offering = odds_entities.OddsOffering(snapshot_timestamp, odds_object)
                        odds_update_builder.add_odds(odds_offering.timestamp, odds_offering.odds)
        return odds_update_builder.build()

    def convert_odds_row_to_odds_objects(self, bet_row, sportsbook, game_datetime_obj):
        """Maps columns from the odds table, converts to odds objects and returns tuple (timestamp, odds_object_list)"""

        snapshot_date_str = bet_row[0]
        snapshot_time_str = bet_row[1]
        snapshot_timestamp_ms = convert_row_snapshot_datetime_string_to_timestamps(date_str=snapshot_date_str, time_str=snapshot_time_str, game_datetime_obj=game_datetime_obj)
        fav_money_line =        convert_string_odds_to_odds_object(bet_row[2], sportsbook, "money_line")
        dog_money_line =        convert_string_odds_to_odds_object(bet_row[3], sportsbook, "money_line")
        fav_spread =            convert_string_odds_to_odds_object(bet_row[4], sportsbook, "spread")
        dog_spread =            convert_string_odds_to_odds_object(bet_row[5], sportsbook, "spread")
        total_over =            convert_string_odds_to_odds_object(bet_row[6], sportsbook, "total_over")
        total_under =           convert_string_odds_to_odds_object(bet_row[7], sportsbook, "total_under")
        fav_fst_half =          convert_string_odds_to_odds_object(bet_row[8], sportsbook, "half")
        dog_fst_half =          convert_string_odds_to_odds_object(bet_row[9], sportsbook, "half")
        fav_snd_half =          convert_string_odds_to_odds_object(bet_row[10], sportsbook, "half")
        dog_snd_half =          convert_string_odds_to_odds_object(bet_row[11], sportsbook, "half")

        list_of_odds = [fav_money_line, dog_money_line, fav_spread, dog_spread,
                        total_over, total_under, fav_fst_half, dog_fst_half,
                        fav_snd_half, dog_snd_half]

        return snapshot_timestamp_ms, list_of_odds

def extract_game_meta_data(table_list):
    """Extracts game meta data from heads of tables, returns tuple"""
    away_team, home_team = table_list[0][0][0].split(' @ ')
    game_time_str = table_list[1][1][0][10:]
    game_date_str = table_list[1][0][0][10:]
    game_timestamp_ms, game_datetime_obj = convert_game_datetime_string_to_timestamp(date_str=game_date_str, time_str=game_time_str)
    return (home_team, away_team, game_timestamp_ms, game_datetime_obj)

class SoupFactory(object):
    """Creates a soup factory object based on the parser chosen, get returns html soup via beautifulsoup"""

    def __init__(self, parser='lxml'):
        self.parser = parser

    def get(self, raw_html):
        return bs(raw_html, self.parser)


class LineTableParser(object):
    """Parses html soup from VI line table pages, strips values from the table and
        returns them to an array of table contents"""

    def __init__(self, html_tag='tbody', class_dict={}, parser='lxml'):
        self.html_tag = html_tag
        self.class_dict = class_dict
        self.soup_factory = SoupFactory(parser)

    def get_tables(self, raw_html):
        """Takes raw_html from line movement pages, strips all data from table
            and returns an array of table data in strings"""
        soup = self.soup_factory.get(raw_html)
        find_tables = soup.find_all(self.html_tag, self.class_dict)
        if find_tables == 0:
            raise ValueError("The passed html is empty or not the expected format, the first 300 lines are:%s" % raw_html[:300])
        table_list = []

        for table in find_tables:
            if is_deepest_table(table, self.html_tag, self.class_dict):
                table_data = []
                rows = table.find_all('tr')
                for row in rows:
                    cols = row.find_all('td')
                    table_data.append([ele.get_text(strip=True) for ele in cols])
                table_list.append(table_data)
        return table_list

def is_deepest_table(table, html_tag, class_dict):
    """Returns True if no child tables exist"""
    if len(table.find_all(html_tag, class_dict)) == 0:
        return True
    return False

money_line_regx = re.compile(r'^([A-Z]{3})\s?([\+\-]\d+|XX)$')
spread_regx     = re.compile(r'^([A-Z]{3})(PK|XX|[\+\-]?\d+\.?\d?)\s*(XX|[\-\+]\d+)$')
total_regx      = re.compile(r'^(\d+\.?\d|XX)\s*([\-\+]\d+|XX)$')
half_regx       = re.compile(r'^([A-Z]{3})(PK|XX|[\+\-]\d+\.?\d?)$')

def convert_string_odds_to_odds_object(string, sportsbook, type):
    """Takes bet strings and regex matches to capture the relevent data,
        returns OddsOffering object, or None if the string is blank, or contains
        a invalid bet/odds string such as XX
        @param string: Odds line strings
        @param sportsbook: The sportsbook offering the odds
        @param type: The bet type"""

    if string == '':
        return None

    if type == "money_line":
        team_symbol, odds = re.findall(money_line_regx, string)[0]
        if odds == 'XX':
            return None
        return odds_entities.MoneyLineOdds(sportsbook, int(odds), team_symbol)

    elif type == "spread":
        team_symbol, spread, odds = re.findall(spread_regx, string)[0]
        if spread == 'XX' or odds == 'XX':
            return None
        if spread == 'PK':
            spread = 0
        return odds_entities.SpreadOdds(sportsbook, int(odds), team_symbol, float(spread))

    elif type == "total_over":
        total, odds = re.findall(total_regx, string)[0]
        type = "OVER"
        if total == 'XX' or odds == 'XX':
            return None
        return odds_entities.TotalOdds(sportsbook, type, int(odds), float(total))

    elif type == "total_under":
        total, odds = re.findall(total_regx, string)[0]
        type = "UNDER"
        if total == 'XX' or odds == 'XX':
            return None
        return odds_entities.TotalOdds(sportsbook, type, int(odds), float(total))

    elif type == "half":
        return None #temp fix until half bet types handled in odds_entities
        team_symbol, odds = re.findall(half_regx, string)[0]
        type = "half"
        if odds == 'XX':
            return None
        if odds == 'PK':
            odds = 0
        return odds_entities.MoneyLineOdds(sportsbook, float(odds), team_symbol)

    else:
        raise ValueError("No matching bet type for %s" % type)

def convert_game_datetime_string_to_timestamp(date_str, time_str):
    """Converts the game date/time string into a timestamp and datetime object"""

    naive_game_time = dt.datetime.strptime(time_str, "%I:%M %p").time()
    game_date = dt.datetime.strptime(date_str, "%A, %B %d, %Y")
    tz = pytz.timezone('US/Eastern')
    game_naive_datetime = dt.datetime(game_date.year,
                                      game_date.month,
                                      game_date.day,
                                      naive_game_time.hour,
                                      naive_game_time.minute)
    datetime = tz.localize(game_naive_datetime)
    timestamp = int(datetime.timestamp() * 1000)
    return timestamp, datetime #return datetime because row snapshots need some place to get year from, dunno if this is ideal

def convert_row_snapshot_datetime_string_to_timestamps(date_str, time_str, game_datetime_obj):
    """Converts the line date/time string to a timestamp"""

    line_snapshot_year = game_datetime_obj.year
    tz = pytz.timezone('US/Eastern')
    line_snapshot_month_str, line_snapshot_day_str = date_str.split(r"/")
    line_snapshot_time = dt.datetime.strptime(time_str, "%I:%M%p").time()
    line_snapshot_datetime = dt.datetime(line_snapshot_year,
                                         int(line_snapshot_month_str),
                                         int(line_snapshot_day_str),
                                         line_snapshot_time.hour,
                                         line_snapshot_time.minute)
    datetime = tz.localize(line_snapshot_datetime)
    timestamp = int(datetime.timestamp() * 1000) #Convert to ms
    return timestamp
