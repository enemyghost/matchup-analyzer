from bs4 import BeautifulSoup

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

