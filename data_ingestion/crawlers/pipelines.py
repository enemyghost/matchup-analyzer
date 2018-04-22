# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from data_ingestion.dao import odds_dao

class PostgresPipeline(object):
  def process_item(self, item, spider):
    odds_dao.upsert_line_url(url=item['url'], vendor_id=item['vendor_id'], sport_name=item['sport'])
    return item
