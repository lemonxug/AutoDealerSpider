# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
from AutoDealerSpider.spiders.areas import provinceCityDatas
import json


class ChanganSpider(scrapy.Spider):
    name = 'changan'
    allowed_domains = ['changan.com.cn']
    start_urls = ['http://changan.com.cn/']

    def parse(self, response):
        for p in provinceCityDatas.values():
            if len(p['child']) == 0:
                continue
            for k, v in p['child'].items():
                next_page = 'https://www.changan.com.cn/cache/dealer/dealer_{}_json.js'.format(k)
                yield scrapy.Request(next_page, callback=self.parse_dlr,
                                 cb_kwargs=dict(province=p['name'], city=v['name']))

    def parse_dlr(self, response, province, city):
        dlrs = json.loads(response.text[18:-1])
        for dlr in dlrs:
            # print(dlr['map_position'])
            dealer = {
                '编号': dlr['dealer_code'],
                '省份': province,
                '城市': city,
                '县区': '',
                '品牌': self.name,
                '公司名称': dlr['dealer_name'],
                '联系电话': dlr['contact_phone'],
                '地址': dlr['address'],
                '经度': dlr['map_position'].split(',')[0].strip() if dlr['map_position'] else '',
                '纬度': dlr['map_position'].split(',')[1].strip() if dlr['map_position'] else '',
                '坐标': dlr['map_position'],
                'crawlTime': datetime.today(),
            }
            yield dealer

