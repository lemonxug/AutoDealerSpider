# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
import json


class WeySpider(scrapy.Spider):
    name = 'wey'
    allowed_domains = ['wey.com']
    start_urls = ['https://www.wey.com/index.php?m=tiyan&c=index&a=province']

    def parse(self, response):
        for i in json.loads(response.text):
            p = i['province']
            c = i['city']
            next_page = 'https://www.wey.com/index.php?m=tiyan&c=index&a=distributor' \
                        '&b={}&t='.format(c)
            yield scrapy.Request(next_page, callback=self.parse_dlr,
                                 cb_kwargs=dict(p=p, c=c))

    def parse_dlr(self, response, p ,c):
        dlrs = json.loads(response.text)
        for dlr in dlrs:
            dealer = {
                '编号': dlr['id'],
                '省份': p,
                '城市': c,
                '县区': '',
                '品牌': self.name,
                '公司名称': dlr['sh_serviceStoreName'],
                '联系电话': dlr['sh_saleHotline'],
                '地址': dlr['sh_address'],
                '经度': dlr['sh_longitude'],
                '纬度': dlr['sh_latitude'],
                '坐标': '{}, {}'.format(dlr['sh_longitude'],dlr['sh_latitude']),
                'crawlTime': datetime.today(),
            }
            yield dealer
