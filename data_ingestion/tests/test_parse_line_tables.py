import unittest
import sys, os
from data_ingestion.crawlers.spiders import parse_line_tables as parser
from bs4 import BeautifulSoup as bs

test_file_path = "data_ingestion/tests/fixtures/cavs_at_celts_request.html"

class Test_LineTableParser(unittest.TestCase):
    html_parsers = ["lxml"]

    def test_LineTableParser(self):
        for html_parser in self.html_parsers:
            with open(test_file_path) as test_html_file:

                test_html_bytes = test_html_file.read().encode('utf-8')
                test_parser = parser.LineTableParser(parser=html_parser)
                output = test_parser.get_tables(test_html_bytes)
                total_cells = 0
                table_number = 0
                for table in output:
                    table_number += 1
                    total_cells += len(table)

                self.assertEqual(total_cells, 606)

    def test_game_data_factory(self):
        with open(test_file_path) as test_html_file:
            test_html_bytes = test_html_file.read().encode('utf-8')
            sport_id = 1
            vendor_id = 1
            html_parser = 'lxml'
            game_data_factory= parser.GameDataFactory(sport_id, vendor_id, html_parser)
            output = game_data_factory.build_game_data(test_html_bytes)

            self.assertEqual((output.home_team, output.away_team, output.game_timestamp, len(output.odds_list)),
                             ('Boston Celtics', 'Cleveland Cavaliers', 1527467700000, 826))
                             
    @unittest.skip("Only useful for comparing different parsing engines")
    def test_Parsers(self):
        for html_parser in self.html_parsers:
            with open(test_file_path) as test_html_file:
                test_html_bytes = test_html_file.read().encode('utf-8')
                soup = bs(test_html_bytes, html_parser)
                tables = soup.find_all('tbody')
                print(html_parser, "found:", len(tables), "tables")


if __name__ == '__main__':
     unittest.main()
