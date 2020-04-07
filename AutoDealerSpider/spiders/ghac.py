# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
import requests
import json


class GhacSpider(scrapy.Spider):
    name = 'ghac'
    allowed_domains = ['ghac.cn']
    start_urls = ['https://www.ghac.cn/Ajax/DealerHandler.ashx?module=GetDealers']

    def parse(self, response):
        for dlr in json.loads(response.text):
            dealer = {
                '编号': dlr['DEALER_CODE'],
                '省份': '',
                '城市': '',
                '县区': '',
                '品牌': self.name,
                '公司名称': dlr['REGISTRATION_NAME'],
                '联系电话': dlr['SALES_PHONE'],
                '地址': dlr['ADDRESS'],
                '经度': dlr['LONGITUDE'],
                '纬度': dlr['LATITUDE'],
                '坐标': '{}, {}'.format(dlr['LONGITUDE'], dlr['LATITUDE']),
                'crawlTime': datetime.today(),
            }
            yield dealer
