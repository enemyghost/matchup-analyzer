import sys
import cProfile
# Add the parent dir to the syspath
sys.path.insert(0,'..')

import html_parser, html_fetcher

test_urls = ["http://www.vegasinsider.com/college-basketball/odds/las-vegas/line-movement/loyola-chicago-@-michigan.cfm/date/3-31-18/time/1805#BT", "http://www.vegasinsider.com/nba/odds/las-vegas/line-movement/bucks-@-warriors.cfm/date/3-29-18/time/2235#AA",
           "http://www.vegasinsider.com/nba/odds/las-vegas/line-movement/grizzlies-@-trail-blazers.cfm/date/4-01-18/time/2105#L", 'http://www.vegasinsider.com/nhl/odds/las-vegas/line-movement/canadiens-@-penguins.cfm/date/3-31-18/time/1910#BT']

out = []
for test_url in test_urls:

    Html_Parser = html_parser.HtmlParser()

    Html = html_fetcher.HtmlFetcher().fetch(test_url).content

    output = Html_Parser.get_tables(Html)

    out.append(test)

for result in out:
    print(result.teams, result.game_time, [key for key in result.line_dict])
