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

    Html_Parser = html_parser.HtmlParser()

    Html = html_fetcher.HtmlFetcher().fetch(test_url['url']).content

    output = Html_Parser.get_tables(Html)

    out.append(output)


for result in out:

    with open(result.away_team + ' at ' + result.home_team + '.csv', 'w', newline='') as f:
        w = csv.writer(f, delimiter=',', quotechar='"')
        for key in result.line_dict.keys():
            for row in [result.line_dict[key][x,:] for x in range(result.line_dict[key].shape[0])]:
                w.writerow([key] + row.tolist())