from html_fetcher import HtmlFetcher
from bs4 import BeautifulSoup


url = "http://www.vegasinsider.com/nba/odds/las-vegas/line-movement/bucks-@-warriors.cfm/date/3-29-18/time/2235#AA"


raw_html = HtmlFetcher().get_html(url).content

class GetSoup(object):
    """Accepts html and outputs soup"""
    def __init__(self, parser="lxml"):
        self.parser = parser

    def get_soup(self, raw_html):
        return BeautifulSoup(raw_html, self.parser)


class ParseTables(object):
    """Parses html soup for tables with html_tag and optional class:value dict to narrow down to specific tables"""

    def __init__(self, html_tag="tbody", class_dict={}):
        self.html_tag = html_tag
        self.class_dict = class_dict

    def get_tables(self, soup):
        find_tables = soup.find_all(self.html_tag, self.class_dict)
        data_out = []
        for table in find_tables:
            table_data = []
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                table_data.append([ele.get_text(strip = True) for ele in cols])
            data_out.append(table_data)

        return data_out


print(ParseTables().get_tables(GetSoup().get_soup(raw_html)))











       



