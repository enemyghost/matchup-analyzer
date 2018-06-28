import scrapy
import os

class HtmlPersister(scrapy.Spider):
    name = "html_persister"

    def __init__(self, url):
        self.url = url

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response):
        file_name = response.request.url.replace(r'/','_') + ".html"
        save_path = './tests/fixtures'
        file_dir = os.path.join(save_path, file_name)
        with open(file_dir, 'w') as f:
            f.write(response.text)
