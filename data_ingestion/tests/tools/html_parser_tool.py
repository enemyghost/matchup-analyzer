import sys
import os
import csv
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

    html_parser.GameDataCSVPersister(output).to_csv()