# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class AutodealerspiderPipeline(object):
    def process_item(self, item, spider):
        return item


from scrapy.exceptions import DropItem
class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['编号'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['编号'])
            return item


from sqlalchemy import create_engine
import pandas as pd
class CarpricespiderPipeline(object):

    def __init__(self):
        # pip install pymysql
        # pip install mysqlclient 未安装会报错
        self.engine = create_engine('mysql://root:root@localhost:3306/carprice?charset=utf8', echo=False)

    def process_item(self, item, spider):
        df = pd.DataFrame([item,])
        df.to_sql(name=spider.name, con=self.engine, if_exists='append', index=None, chunksize=10000)
        return item

    def close_spider(self, spider):#关闭爬虫时
        pass


from datetime import date
class ExportToXlsx(object):

    def __init__(self):
        self.path = 'Data'
        self.data = pd.DataFrame()
        self.today = date.strftime(date.today(), '%Y%m%d')

    def process_item(self, item, spider):
        df = pd.DataFrame([item,])
        self.data = pd.concat([self.data, df])
        return item

    def close_spider(self, spider):#关闭爬虫时
        if self.path != '.':
            import os
            os.makedirs(self.path, 777, 1)
        filename = '{}/{}_{}.xlsx'.format(self.path, spider.name, self.today )
        self.data.to_excel(filename, index=None)


import requests
import logging
class AddressPraser(object):

    def __init__(self):
        self.s = requests.Session()
        self.ak = '****'
        self.translate_api = 'http://api.map.baidu.com/geoconv/v1/?coords={}&from=5&to=6&ak={}'
        self.poi_api = 'http://api.map.baidu.com/?qt=rgc&x={}&y={}&dis_poi=100&poi_num=10&' \
                  'latest_admin=1&ak={}'

    def process_item(self, item, spider):
        if (item['县区'] == '') and item['坐标'] :
            r = self.s.get(self.translate_api.format(item['坐标'], self.ak),)
            xy = r.json()['result'][0]
            r = self.s.get(self.poi_api.format(xy['x'], xy['y'], self.ak),)
            address =  r.json()['content']
            item['县区'] = address['address_detail']['district']
            if item['地址'] == '':
                item['地址'] = address['address']
            print('地址处理：', item)
            logging.info('地址处理：'+str(item))
            return item
        else:
            return item

    def close_spider(self, spider): #关闭爬虫时
        pass
