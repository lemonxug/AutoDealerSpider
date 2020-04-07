# -*- coding: utf-8 -*-
import scrapy
import json
import requests
from datetime import datetime


class GactoyotaSpider(scrapy.Spider):
    name = 'gactoyota'
    allowed_domains = ['gac-toyota.com.cn']
    start_urls = ['https://www.gac-toyota.com.cn/js/newprovincecitydealer/data/dealerData.js',]

    def parse(self, response):
        def to_dict(self, data):
            t_dict = {}
            for i in data:
                t_dict[i['value']] = i
            return t_dict
        pr = requests.get('https://www.gac-toyota.com.cn/js/newprovincecitydealer/data/provinceData.js')
        cr = requests.get('https://www.gac-toyota.com.cn/js/newprovincecitydealer/data/cityData.js')
        province = json.loads(bytes.decode(pr.content)[19:])
        city = json.loads(bytes.decode(cr.content)[16:])
        province = to_dict(province)
        city = to_dict(city)

        dlrs = json.loads(response.text[17:])
        for dlr in dlrs:
            dealer = {
                '编号': dlr['DealerCode'],
                '省份': province[city[dlr['City']]['parent']]['name'],
                '城市': city[dlr['City']]['name'],
                '县区': '',
                '品牌' : self.name,
                '公司名称':dlr['DealerName'],
                '联系电话':dlr['Tel'],
                '地址':dlr['Address'],
                '经度':dlr['Longitude'],
                '纬度':dlr['Latitude'],
                '坐标':dlr['Longitude']+','+dlr['Latitude'],
                'crawlTime': datetime.today(),
            }
            yield dealer
