import sys
import csv
import cProfile
# Add the parent dir to the syspath
sys.path.insert(0,r'\matchup-analyzer\data-ingestion')

import html_parser, html_fetcher

urls = csv.DictReader(open('test_links.csv', 'r'))
out = []
for test_url in urls:

    Html_Parser = html_parser.HtmlParser()

    Html = html_fetcher.HtmlFetcher().fetch(test_url['url']).content

    output = Html_Parser.get_tables(Html)

    out.append(output)


for result in out:
    print(result.home_team, result.away_team, result.game_time, result.game_date, [key for key in result.line_dict])
