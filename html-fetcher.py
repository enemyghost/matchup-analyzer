import unittest
import urllib.request

class HtmlFetcher(object):

	def __init__(self, number_of_tries=1, proxy_list=[]):
		self.number_of_tries = number_of_tries
		self.proxy_list = proxy_list


	def get_html(self, url_string):
		"""Takes in a url string and returns html string if possible"""
		#Chrome version 60 user agent
		user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
		header = {'User-Agent': user_agent}
		req = urllib.request.Request(url_string, headers=header)
		for unused in range(self.number_of_tries):
			try:
				response = urllib.request.urlopen(req)

			except urllib.error.URLError as error:
				return error.reason

			except urllib.error.HTTPError as http_error:
				return http_error.reason

		return response.read().decode(response.headers.get_content_charset())

class TestHtmlFetcher(unittest.TestCase):
	def test(self):
		self.assertEqual(HtmlFetcher().get_html("http://ec2-54-174-172-97.compute-1.amazonaws.com/"), "oh god help")

if __name__ == '__main__':
    unittest.main()
