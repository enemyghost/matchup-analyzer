import csv
import sys
import os
import numpy
sys.path.insert(0,r'D:\Users\Code\matchup-analyzer\data_ingestion')

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_path = r"D:\Users\Code\matchup-analyzer\data_ingestion\tests\fixtures\line_links_output.csv"
abs_file_path = os.path.join(script_dir, rel_path)

import html_fetcher, html_parser

urls = csv.DictReader(open(abs_file_path, 'r'))
out = []
for test_url in urls:

    test_parser = html_parser.HtmlParser()

    test_html = html_fetcher.HtmlFetcher().fetch(test_url['url']).content

    output = test_parser.get_tables(test_html)

    out.append(output)


for result in out:

    with open(result.away_team + '_at_' + result.home_team + '_' + result.game_date + '.csv', 'w', newline='') as f:
        w = csv.writer(f, delimiter=',', quotechar='"')
        for key in result.line_dict.keys():
            for row in [result.line_dict[key][x,:] for x in range(result.line_dict[key].shape[0])]:
                w.writerow([key] + row.tolist())