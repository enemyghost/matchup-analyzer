import sys
# Add the parent dir to the syspath
sys.path.insert(0,'..')

import html_parser, html_fetcher
import numpy

test_url = "http://www.vegasinsider.com/nba/odds/las-vegas/line-movement/bucks-@-warriors.cfm/date/3-29-18/time/2235#AA"

Html_Parser = html_parser.HtmlParser()

Html = html_fetcher.HtmlFetcher().fetch(test_url).content

Soup = html_parser.GetSoup().get_soup(Html)

output = Html_Parser.get_tables(Soup)


Bucks = html_parser.ExtractGameData(output)

print(Bucks.team_a, Bucks.team_b, Bucks.game_time, Bucks.game_date, Bucks.line_dict['ATLANTIS'])








