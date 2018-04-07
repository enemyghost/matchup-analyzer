from bs4 import BeautifulSoup as bs
import numpy as np
import datetime
import csv
import os

class SoupFactory(object):
    """Accepts html and outputs soup"""

    def __init__(self, parser):
        self.parser = parser

    def get(self, raw_html):
        return bs(raw_html, self.parser)


class HtmlParser(object):
    """Parses html soup for html_tag and optional class:value dict"""

    def __init__(self, html_tag="tbody", class_dict={}, parser='lxml'):
        self.html_tag = html_tag
        self.class_dict = class_dict
        self.soup_factory = SoupFactory(parser)

    def get_tables(self, raw_html):
        """Passes 3d list of all tables stripped contents"""
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
    """Extracts game data from table and returns created GameData object"""
    teams = table_list[0][0][0].split(' @ ')
    away_team = teams[0]
    home_team = teams[-1]
    game_time = table_list[1][1][0][10:]
    string_date = table_list[1][0][0][10:]
    game_date = datetime.datetime.strptime(string_date, "%A, %B %d, %Y").strftime("%m-%d-%Y")
    return GameData(home_team, away_team, game_time, game_date, create_dict(table_list))

class GameData(object):
    """"GameData object with a dictionary of arrays for each sportsbooks line movement data"""
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

class GameDataCSVPersister(object):
    """"Taks a GameData object and saves it to CSV file"""

    def __init__ (self, game_data):
        self.game_data = game_data

    def to_csv (self):
        filename = '/output/' + self.game_data.away_team + '_at_' + self.game_data.home_team + '_' + self.game_data.game_date + '.csv'
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w', newline='') as f:
            w = csv.writer(f, delimiter=',', quotechar='"')
            for key in self.game_data.line_dict.keys():
                for row in [self.game_data.line_dict[key][x, :] for x in range(self.game_data.line_dict[key].shape[0])]: #iterates through rows of line data array
                    w.writerow([key] + row.tolist())