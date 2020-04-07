# -*- coding: utf-8 -*-
import scrapy
import json
from datetime import datetime


class GeelySpider(scrapy.Spider):
    name = 'geely'
    allowed_domains = ['geely.com']
    start_urls = ['https://www.geely.com/api/geely/official/get/getprovincelist']
    header = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; ZoomSpider.net bot; .NET CLR 1.1.4322)',
        'Referer': 'ttps://www.geely.com',
    }

    def parse(self, response):
        provinces = json.loads(response.text)
        for p in provinces:
            next_page = 'https://www.geely.com/api/geely/official/get/getcitylist?provinceid={}'.format(p['regionId'])
            yield response.follow(next_page, callback=self.parse_city,
                                  cb_kwargs=dict(province=p))

    def parse_city(self, response, province):
        citys = json.loads(response.text)
        for c in citys:
            next_page = 'https://www.geely.com/api/geely/official/get/' \
                        'GetDealer?seriesCode=&province={}&city={}&keyword='.format(province['regionId'], c['regionId'])
            yield response.follow(next_page, callback=self.parse_dlr,
                                  cb_kwargs=dict(province=province, city=c))

    def parse_dlr(self, response, province, city):
                dealers = json.loads(response.text)
                for dlr in dealers:
                    if dlr['dealerId'] == 16180:
                        dlr['coordinates'] = '116.376747,40.018948'
                    dealer = {
                        '编号': dlr['dealerId'],
                        '省份': province['regionName'],
                        '城市': city['regionName'],
                        '县区': '',
                        '品牌': self.name,
                        '公司名称': dlr['dealerName'],
                        '联系电话': dlr['bizPhone'],
                        '地址': dlr['address'],
                        '经度': dlr['coordinates'][:11] if dlr['coordinates'] else '',
                        '纬度': dlr['coordinates'][11:] if dlr['coordinates'] else '',
                        '坐标': dlr['coordinates'],
                        'crawlTime': datetime.today(),
                    }
                    yield dealer
