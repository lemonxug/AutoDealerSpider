# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
import json

class ChevroletSpider(scrapy.Spider):
    name = 'chevrolet'
    allowed_domains = ['www.chevrolet.com.cn']
    start_urls = ['https://www.chevrolet.com.cn/data/dealer.json']

    def parse(self, response):
        data = json.loads(response.text)
        for p in data:
            for c in p['data']:
                for dlr in c['data']:
                    dealer = {
                        '编号': dlr['id'],
                        '省份': p['name'],
                        '城市': c['name'],
                        '县区': '',
                        '品牌': self.name,
                        '公司名称': dlr['name'],
                        '联系电话': dlr['phone'],
                        '地址': dlr['addr'],
                        '经度': dlr['retlng'].split(', ')[0],
                        '纬度': dlr['retlng'].split(', ')[1],
                        '坐标': dlr['retlng'],
                        'crawlTime': datetime.today(),
                        }
                    yield dealer
