import sys, os
sys.path.insert(0,'..')
import unittest
from crawlers.spiders import parse_line_tables as parser

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_paths = r"fixtures\celtics-vs-cavaliers052118.html"


class TestParseLineTables(unittest.TestCase):
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, 'r') as test_file:
        html = test_file.read()
        TestParser = parser.HtmlParser(html_tag='tbody', class_dict={}, parser='lxml')
        output = TestParser.get_tables(html)



    def test(self):
        self.assertEqual(output.away_team, "Boston Celtics")

if __name__ == '__main__':
     unittest.main()
