from bs4 import BeautifulSoup
import numpy


class GetSoup(object):
    """Accepts html and outputs soup"""
    def __init__(self, parser="lxml"):
        self.parser = parser

    def get_soup(self, raw_html):
        return BeautifulSoup(raw_html, self.parser)


class HtmlParser(object):
    """Parses html soup for html_tag and optional class:value dict"""

    def __init__(self, html_tag="tbody", class_dict={}):
        self.html_tag = html_tag
        self.class_dict = class_dict

    def get_tables(self, soup):
        find_tables = soup.find_all(self.html_tag, self.class_dict)
        data_out = []
        for table in find_tables:
            if is_deepest_table(table, self.html_tag, self.class_dict):
                table_data = []
                rows = table.find_all('tr')
                for row in rows:
                    cols = row.find_all('td')
                    table_data.append([ele.get_text(strip = True) for ele in cols])
                data_out.append(table_data)

        return data_out


def is_deepest_table(table_soup, html_tag, class_dict):
    if len(table_soup.find_all(html_tag, class_dict)) == 0:
        return True
    return False



class ExtractGameData(object):
    """"Creates a GameData object with a dictionary of arrays for each sportsbook"""

    def __init__(self, parsed_table):
        self.parsed_table = parsed_table
        self.teams = parsed_table[0][0][0]
        self.team_a = self.teams.split(' @ ')[0]
        self.team_b = self.teams.split(' @ ')[-1]
        self.game_time = parsed_table[1][1][0][10:]
        self.game_date = parsed_table[1][0][0][10:]
        self.line_dict = {}
        self.create_dict()

    def create_dict(self):
        for table in self.parsed_table[2:]:
            if len(table[0]) == 1:
                sportsbook_name = table[0][0][:-15]
            self.line_dict[sportsbook_name] = numpy.array(table[2:])

