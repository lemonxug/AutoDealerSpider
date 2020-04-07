# -*- coding: utf-8 -*-
import scrapy
import json
from datetime import datetime


class FtmsSpider(scrapy.Spider):
    name = 'ftms'
    allowed_domains = ['ftms.com.cn']
    start_urls = ['https://www.ftms.com.cn/website/Maintenance/getProvince']

    def parse(self, response):
        province = json.loads(response.text)
        for province in province['data']:
            next_page = 'https://www.ftms.com.cn/website/Maintenance/getCity?cid={}'.format(province['cid'])
            yield response.follow(next_page, callback=self.parse_city,
                                  cb_kwargs=dict(province=province))

    def parse_city(self, response, province):
            for city in json.loads(response.text)['data']:
                post_data = {"cityid": city['cid'], "cityName": "",
                             "dealerName": "",
                             "provinceid": province['cid'], "provinceName": ""}
                next_page = 'https://www.ftms.com.cn/website/Dealer/getDealer'
                yield scrapy.Request(next_page, callback=self.parse_dlr,
                                     method='POST',body=json.dumps(post_data),)

    def parse_dlr(self, response):
        for dlr in json.loads(response.text)['data']['list']:
            dealer = {
                '编号': dlr['id'],
                '省份': dlr['province'],
                '城市': dlr['city'],
                '县区': '',
                '品牌': self.name,
                '公司名称': dlr['fullname'],
                '联系电话': dlr['phone_seal'],
                '地址': dlr['address'].strip(),
                '经度': dlr['lng'],
                '纬度': dlr['lat'],
                '坐标': dlr['lng'] + ',' + dlr['lat'],
                'crawlTime': datetime.today(),
            }
            yield dealer

