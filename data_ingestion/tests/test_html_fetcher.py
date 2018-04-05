import unittest
import sys, os
sys.path.insert(0,'..')
import html_fetcher

class TestHtmlFetcher(unittest.TestCase):
    def test(self):
        self.assertEqual(html_fetcher.HtmlFetcher().fetch("http://www.google.com").code, 200)
        self.assertEqual(html_fetcher.HtmlFetcher().fetch("http://www.yahoo.com/dicks").code, 404)




if __name__ == '__main__':
     unittest.main()