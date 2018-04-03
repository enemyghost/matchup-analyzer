import unittest
import html_fetcher

class TestHtmlFetcher(unittest.TestCase):
    def test(self):
        self.assertEqual(HtmlFetcher().get_html("http://www.google.com").code, 200)
        self.assertEqual(HtmlFetcher().get_html("http://www.yahoo.com/dicks").code, 404)




if __name__ == '__main__':
     unittest.main()