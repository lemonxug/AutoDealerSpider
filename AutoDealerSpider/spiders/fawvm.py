# -*- coding: utf-8 -*-
import scrapy
import json
from datetime import datetime


class FawvmSpider(scrapy.Spider):
    name = 'fawvm'
    allowed_domains = ['faw-vw.com']
    start_urls = ['http://contact.faw-vw.com/uploadfiles/js/dealer.js']

    def parse(self, response):
        s = response.text.replace(u'\xa0', '')[16:]
        dlrs = json.loads(s)
        for dlr in dlrs:
            dealer = {
                '编号': dlr['vd_dealerCode'],
                '省份': dlr['vp_name'].split()[1],
                '城市': dlr['vc_name'],
                '县区': '',
                '品牌': self.name,
                '公司名称': dlr['vd_dealerName'],
                '联系电话': dlr['vd_salePhone'],
                '地址': dlr['vd_address'],
                '经度': dlr['vd_longitude'],
                '纬度': dlr['vd_latitude'],
                '坐标': dlr['vd_longitude'] + ',' + dlr['vd_latitude'],
                'crawlTime': datetime.today(),
            }
            yield dealer