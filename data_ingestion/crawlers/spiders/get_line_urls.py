# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime, timedelta

class VILineURLSpider(scrapy.Spider):
    name = 'get_line_urls'

    def __init__(self, sport, start_date, end_date, season_year=None):
        self.sport = sport
        self.start_date = start_date #date for nba, week number for nfl
        self.end_date = end_date #date for nba, week number for nfl
        self.season_year = season_year #for nfl

    def create_url_scheme(self):
        domain = "http://www.vegasinsider.com/"
        list_of_urls = []

        if self.sport == 'nba':
            for date in date_range(self.start_date, self.end_date):
                list_of_urls.append("{}{}/scoreboard/scores.cfm/game_date/{}".format(domain, self.sport, date))
            return list_of_urls

        elif self.sport == 'nfl':
            if self.season_year == None:
                raise ValueError("You must include a season year for NFL line discovery")
            for week in week_range(self.start_date, self.end_date):
                list_of_urls.append("{}{}/scoreboard/scores.cfm/week/{}/season/{}".format(domain, self.sport, week, self.season_year))
        return list_of_urls

    def start_requests(self):
        for url in self.create_url_scheme():
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for url in response.xpath('//a[contains(@href,"line-movement")]/@href').extract():
            yield {'url':'http://www.vegasinsider.com' + url, 'sport': self.sport, 'vendor_id': 1}

def week_range(start_week, end_week):
    curr_week = int(start_week)
    pre_dict = {-5:-1, -4: -2, -3: -3, -2: -4, -1: -5} #convert to VI retarded preseason numbering format
    while curr_week <= int(end_week):
        if curr_week < 0:
            yield pre_dict[curr_week]
        elif curr_week > 0:
            yield curr_week
        curr_week += 1

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
