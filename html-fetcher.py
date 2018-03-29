import unittest
import urllib.request


class HtmlFetcher(object):
    """Return HTTPResponse object"""
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'

    def __init__(self, number_of_tries=1, proxy=None):
        self.number_of_tries = number_of_tries
        self.proxy = proxy

    def get_html(self, url_string):
        """Takes in a url string and returns html string if possible"""
        # Chrome version 60 user agent
        header = {'User-Agent': HtmlFetcher.user_agent}
        req = urllib.request.Request(url_string, headers=header)

        if self.proxy is not None:
        	handler = urllib.request.ProxyHandler(proxy)
        	opener = urllib.request.build_opener(handler)
        	urllib.request.install_opener(opener)

        for n in range(1, self.number_of_tries + 1):
            try:
                response = urllib.request.urlopen(req)
                content = response.read().decode(response.headers.get_content_charset())
                code = response.code
                return HttpResponse(code, content)

            except urllib.error.URLError as error:
                if n == self.number_of_tries:
                    return HttpResponse(error.code, error.reason)

            except urllib.error.HTTPError as http_error:
                if n == self.number_of_tries:
                    return HttpResponse(http_error.code, http_error.reason)

            except IOError:
            	return "Bad Proxy?"


        

class HttpResponse(object):
    """Http response object with params code, content"""

    def __init__(self, code, content):
        self.code    = code
        self.content = content

class TestHtmlFetcher(unittest.TestCase):
    def test(self):
        self.assertEqual(HtmlFetcher().get_html("http://ec2-54-174-172-97.compute-1.amazonaws.com/").content, "oh god help")
        self.assertEqual(HtmlFetcher().get_html("http://www.yahoo.com/dicks").code, 404)


if __name__ == '__main__':
     unittest.main()