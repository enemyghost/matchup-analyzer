import unittest
import sys, os
from data_ingestion.crawlers.spiders import parse_line_tables as parser
from bs4 import BeautifulSoup as bs
import scrapy

test_file_path = "data_ingestion/tests/fixtures/cavs_at_celts_request.html"

class Test_LineTableParser(unittest.TestCase):
    parsers = ["lxml", "html5lib", "html.parser"]

    def test_LineTableParser(self):
        for parser in self.parsers:
            with open(test_file_path) as test_html_file:

                test_html_bytes = test_html_file.read().encode('utf-8')
                soup = bs(test_html_bytes, parser)
                tables = soup.find_all('tbody')
                print(parser, "found:", len(tables), "tables")

            # test_parser = parser.LineTableParser()
            # output = test_parser.get_tables(test_html)
            #print(output)


if __name__ == '__main__':
     unittest.main()
