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




for tables in output:
    if len(tables) == 1:
        print(tables)
    if len(tables) == 2:
        print(tables[0][0])
        print(tables[0][1])
        print(tables[0][2])
    else:
        print(tables[:2])
        print(numpy.array2string(numpy.array(tables[2:]), max_line_width=numpy.inf))









