# -*- coding: utf-8 -*-
import scrapy
import json
from datetime import datetime


class BuickSpider(scrapy.Spider):
    name = 'buick'
    allowed_domains = ['buick.com.cn']
    start_urls = ['http://www.buick.com.cn/api/dealer.aspx']

    def parse(self, response):
        dlrs = json.loads(response.text.replace(u'\xa0', u''))
        for dlr in dlrs:
            dealer = {
                '编号': dlr['dealerCode'],
                '省份': dlr['provinceName'],
                '城市': dlr['cityName'],
                '县区': dlr['districtName'],
                '品牌' : self.name,
                '公司名称':dlr['dealerName'],
                '联系电话':dlr['tel'],
                '地址':dlr['address'],
                '经度':dlr['lng'],
                '纬度':dlr['lat'],
                '坐标':dlr['lng']+','+dlr['lat'],
                'crawlTime': datetime.today(),
            }
            yield dealer

