import unittest
from html_fetcher import *

class TestHtmlFetcher(unittest.TestCase):
    def test(self):
        self.assertEqual(HtmlFetcher().get_html("http://ec2-54-174-172-97.compute-1.amazonaws.com/").content, "oh god help")
        self.assertEqual(HtmlFetcher().get_html("http://www.yahoo.com/dicks").code, 404)
        self.assertEqual(HtmlFetcher(proxy = 'http://50.233.137.37:80').get_html("http://ec2-54-174-172-97.compute-1.amazonaws.com/").content, "oh god help")
        self.assertEqual(HtmlFetcher(proxy = 'http://50.233.137.37:80').get_html("http://www.yahoo.com/dicks").code, 404)


if __name__ == '__main__':
     unittest.main()