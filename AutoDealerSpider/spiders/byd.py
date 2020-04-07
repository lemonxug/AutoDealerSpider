# -*- coding: utf-8 -*-
import scrapy
import json
from datetime import datetime

class BydSpider(scrapy.Spider):
    name = 'byd'
    allowed_domains = ['bydauto.com.cn']
    start_urls = ['http://www.bydauto.com.cn/auto/BrandWorld/SearchDealers.html']

    def parse(self, response):
        for c in response.xpath('//option')[1:-2]:
            # print(c.xpath('./@value')[0])
            car = c.xpath('./@value').get()
            next_page = 'http://www.bydauto.com.cn/sites/custom/service/auto/sales?type=getBeforeSaleProvinces&carType=' \
                        '{}'.format(car)
            yield scrapy.Request(next_page, callback=self.parse_province,
                                 cb_kwargs=dict(car=car))

    def parse_province(self, response, car):
        for p in response.xpath('//option'):
            province = p.xpath('./@value').get()
            next_page = 'http://www.bydauto.com.cn/sites/custom/service/auto/sales?type=getBeforeSaleCitys&carType' \
                        '={}&province={}'.format(car, province)
            yield scrapy.Request(next_page, callback=self.parse_city,
                                 cb_kwargs=dict(car=car, province=province))

    def parse_city(self, response, car, province):
        for c in response.xpath('//option'):
            city = c.xpath('./@value').get()
            next_page = 'http://www.bydauto.com.cn/sites/custom/service/auto/sales?type=getBeforeSaleStores&carType' \
                        '={}&province={}&city={}'.format(car, province, city)
            yield scrapy.Request(next_page, callback=self.parse_dlr,
                                 cb_kwargs=dict(car=car, province=province, city=city))

    def parse_dlr(self, response, car, province, city):
        try:
            for dlr in json.loads(response.text):
                dealer = {
                    '编号': dlr['id'],
                    '省份': province,
                    '城市': city,
                    '县区': '',
                    '品牌': self.name,
                    '公司名称': dlr['sjname'],
                    '联系电话': dlr['phone'],
                    '地址': dlr['address'],
                    '经度': dlr['jingdu'],
                    '纬度': dlr['weidu'],
                    '坐标': '{},{}'.format(dlr['jingdu'], dlr['weidu']),
                    'crawlTime': datetime.today(),
                }
                yield dealer
        except:
            pass


