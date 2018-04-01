import sys, os
sys.path.insert(0,'..')
import unittest
import html_parser

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_path = r"fixtures\bucks-vs-warriors-soup-output.txt"
abs_file_path = os.path.join(script_dir, rel_path)

class TestHtmlParser(unittest.TestCase):
    test_file = open(abs_file_path, 'r')
    html = test_file.read()
    sportsbooks = ['ATLANTIS', "CAESARS/HARRAH'S", 'CG TECHNOLOGY', 'COASTS', 'GOLDEN NUGGET', "JERRY'S NUGGET", 'MIRAGE-MGM', 'PEPPERMILL', 'SOUTHPOINT', 'STATIONS', 'STRATOSPHERE', 'TREASURE ISLAND', 'VI CONSENSUS', 'WESTGATE SUPERBOOK', 'WILLIAM HILL', 'WYNN']
    def test(self):
        Html_Parser = html_parser.HtmlParser()
        output = Html_Parser.get_tables(self.html)
        self.assertEqual(output.home_team, "Golden State Warriors")
        self.assertEqual(output.away_team, "Milwaukee Bucks")
        self.assertEqual(output.game_time, "10:40 PM")
        self.assertEqual(output.game_date, "Thursday, March 29, 2018")
        for sportsbook in self.sportsbooks:
            self.assertEqual(sportsbook in output.line_dict, True)
            self.assertEqual(output.line_dict[sportsbook].shape[1], 12)



if __name__ == '__main__':
     unittest.main()
