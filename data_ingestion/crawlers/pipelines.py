# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from data_ingestion.dao import odds_dao

class PostgresPipeline(object):
  def process_item(self, item, spider):
    if spider.name == 'find_line_links':
        odds_dao.upsert_line_url(url=item['url'], vendor_id=item['vendor_id'], sport_name=item['sport'])
        return item
    if spider.name == 'parse_linetables':
        odds_dao.upsert_game_data(vendor_id=item['vendor_id'], sport_id=item['sport_id'], game_data=item['game_data'])
        return item
