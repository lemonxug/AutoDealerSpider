# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
import json


class PeugeotSpider(scrapy.Spider):
    name = 'peugeot'
    allowed_domains = ['peugeot.com.cn']
    start_urls = ['http://dealer.peugeot.com.cn/dealertype.js?v20311525']

    def parse(self, response):
        for p in json.loads(response.text[16:]).values():
            for c in p.values():
                if len(c['dealer']['4S']) == 0:
                    continue
                for dlr in c['dealer']['4S'].values():
                    dealer = {
                        '编号': dlr['dealer_code'],
                        '省份': c['parentname'],
                        '城市': c['name'],
                        '县区': '',
                        '品牌': self.name,
                        '公司名称': dlr['title'],
                        '联系电话': dlr['sales_phone'],
                        '地址': dlr['address'],
                        '经度': dlr['coordinate_y'],
                        '纬度': dlr['coordinate_x'],
                        '坐标': dlr['coordinate_y'] + ',' + dlr['coordinate_x'],
                        'crawlTime': datetime.today(),
                    }
                    yield dealer
