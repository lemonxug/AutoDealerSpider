# -*- coding: utf-8 -*-
import scrapy
import json
from datetime import datetime


class KiaSpider(scrapy.Spider):
    name = 'kia'
    allowed_domains = ['dyk.com.cn']
    start_urls = ['http://www.dyk.com.cn/public/dyk/js/allDealersData.js']

    def parse(self, response):
        dlr_dict = json.loads(response.text[18:])
        for keys, values in dlr_dict.items():
            for dlr in values:
                dealer = {
                    '编号': dlr['经销商代码'],
                    '省份': dlr['province_name'],
                    '城市': dlr['city_name'],
                    '县区': dlr['district_name'],
                    '品牌': self.name,
                    '公司名称': dlr['name'],
                    '联系电话': dlr['sale_phone'],
                    '地址': dlr['address'].replace(u'\xa0', ''),
                    '经度': dlr['place'].split(',')[0],
                    '纬度': dlr['place'].split(',')[1],
                    '坐标': dlr['place'],
                    'crawlTime': datetime.today(),
                }
                yield dealer
