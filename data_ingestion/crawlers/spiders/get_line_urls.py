# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime, timedelta

class LineLinksSpider(scrapy.Spider):
    name = 'get_line_urls'

    def __init__(self, start_date, end_date, sport_name=None):
        self.sport_name = sport_name
        self.start_date = start_date
        self.end_date = end_date

    def start_requests(self): 
        for url in ["http://www.vegasinsider.com/" + self.sport_name + "/scoreboard/scores.cfm/game_date/" + date for date in date_range(self.start_date, self.end_date)]:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for url in response.xpath('//a[contains(@href,"line-movement")]/@href').extract():
            yield {'url':'http://www.vegasinsider.com' + url, 'sport': self.sport_name, 'vendor_id': 1}
            

def date_range(start, end, step=1, date_format="%m-%d-%Y"):
    """
    Creates generator with a range of dates.
    :param start: the start date of the date range
    :param end: the end date of the date range
    :param step: the step size of the dates
    :param date_format: the string format of the dates inputted and returned
    """
    start = datetime.strptime(str(start), date_format)
    end = datetime.strptime(str(end), date_format)
    num_days = (end - start).days
    
    for d in range(0, num_days + step, step):
        date_i = start + timedelta(days=d)
        yield date_i.strftime(date_format)



