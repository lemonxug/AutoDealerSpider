# -*- coding: utf-8 -*-
import scrapy
import re
import json
from datetime import datetime


class SkodaSpider(scrapy.Spider):
    name = 'skoda'
    allowed_domains = ['skoda.com.cn']
    start_urls = ['http://www.skoda.com.cn/assets/js/apps/dealerdata.js']

    def parse(self, response):
        data = response.text
        p1 = re.compile('window.DEALERS_DATA.\w* = ')
        m1 = p1.split(data)
        province = json.loads(m1[2].strip()[:-1])
        city = json.loads(m1[3].strip()[:-1])
        dealer = json.loads(m1[5].strip()[:-1])
        xy = json.loads(m1[6].split(';')[0])

        def to_dict(columns, values):
            t_dict = {}
            for item in values:
                tmp = {}
                for x, y in zip(columns, item):
                    tmp[x] = y
                t_dict[tmp['code']] = tmp
                # print(t_dict)
            return t_dict

        province_dict = to_dict(province['columnNames'], province['data'])
        city_dict = to_dict(city['columnNames'], city['data'])
        dealer_dict = to_dict(dealer['columnNames'], dealer['data'])

        for dlr in dealer_dict.values():
            dealer = {
                '编号': dlr['code'],
                '省份': province_dict[dlr['province_code']]['name'],
                '城市': city_dict[dlr['city_code']]['name'],
                '县区': '',
                '品牌': self.name,
                '公司名称': dlr['name'],
                '联系电话': dlr['phone'],
                '地址': dlr['address'],
                '经度': xy[dlr['code']][1].split(',')[0] if dlr['code'] in xy.keys() else '',
                '纬度': xy[dlr['code']][1].split(',')[1] if dlr['code'] in xy.keys() else '',
                '坐标': xy[dlr['code']][1] if dlr['code'] in xy.keys() else '',
                'crawlTime': datetime.today(),
            }
            yield dealer
