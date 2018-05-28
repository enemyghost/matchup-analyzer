import unittest
import sys, os
from data_ingestion.crawlers.spiders import parse_line_tables as parser
from bs4 import BeautifulSoup as bs
import urllib

test_file_path = "data_ingestion/tests/fixtures/cavaliers_at_celtics_line.html"
#"data_ingestion/tests/fixtures/rockets_at_warriors_line_movements.htm"

class Test_LineTableParser(unittest.TestCase):
    def test_LineTableParser(self):
        with open(test_file_path, 'r', encoding='utf-8') as test_html:
        #with open(test_file_path) as test_html:
            #test_html = test_html_file.read()
            soup_test = bs(test_html.read(), "html5lib")
            print(len(soup_test.find_all("tbody")))

            # test_parser = parser.LineTableParser()
            # output = test_parser.get_tables(test_html)


            #print(output)


if __name__ == '__main__':
     unittest.main()
