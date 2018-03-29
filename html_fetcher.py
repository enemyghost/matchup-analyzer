import urllib.request, urllib.parse

class HtmlFetcher(object):
    """Return HTTPResponse object"""
    # Chrome version 60 user agent
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'

    def __init__(self, number_of_tries=1, proxy=None, timeout=5):
        self.number_of_tries = number_of_tries
        self.proxy = Proxy(proxy) if proxy is not None else None #proxy string in the form 'type://host:port'
        self.timeout = timeout

    def get_html(self, url_string):
        """Takes in a url string and returns HttpResponse object"""
        
        header = {'User-Agent': self.user_agent}
        req = urllib.request.Request(url_string, headers=header)

        if self.proxy is not None:
            req.set_proxy(self.proxy.host, self.proxy.type)

        for n in range(1, self.number_of_tries + 1):
            try:
                response = urllib.request.urlopen(req, timeout=self.timeout)
                content  = response.read().decode(response.headers.get_content_charset())
                code     = response.code
                return HttpResponse(code, content)

            except urllib.error.URLError as error:
                return HttpResponse(error.code, error.reason)

            except urllib.error.HTTPError as http_error:
                if n == self.number_of_tries:
                    return HttpResponse(http_error.code, http_error.reason)

class HttpResponse(object):
    """Http response object with params code, content"""

    def __init__(self, code, content):
        self.code    = code
        self.content = content

class Proxy(object):
    """Takes a proxy string and parses into type and host"""

    def __init__(self, proxy_url):
        parsed        = urllib.parse.urlparse(proxy_url)
        self.type     = parsed.scheme
        self.host     = parsed.netloc

