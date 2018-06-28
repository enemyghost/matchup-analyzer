# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from data_ingestion.dao import odds_store

class PostgresPipeline(object):
  def process_item(self, item, spider):
    if spider.name == 'get_line_urls':
        odds_store.upsert_line_url(url=item['url'], vendor_id=item['vendor_id'], sport_name=item['sport'])
        return item

    if spider.name == 'parse_line_tables':
        game_data = item['game_data']
        odds_store.upsert_game_data(vendor_id=game_data.vendor_id, sport_id=game_data.sport_id, game_data=game_data)
        odds_store.upsert_line_url(url=item['url'], vendor_id=game_data.vendor_id, sport_id=game_data.sport_id, event_time_epoch_ms=game_data.game_timestamp)
        return item
