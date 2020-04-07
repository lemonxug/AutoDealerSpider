# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
import json


class HondaSpider(scrapy.Spider):
    name = 'honda'
    allowed_domains = ['dongfeng-honda.com']
    start_urls = ['http://www.dongfeng-honda.com/dot_query.shtml']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36'
                      ' (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    count = 1

    def parse(self, response):
        for p in response.xpath('.//option')[1:-1]:
            pd = {
                'id':p.xpath('./@province_id').get(),
                'name': p.xpath('./@value').get(),
            }
            # print(pd)
            next_page = 'http://www.dongfeng-honda.com/index/get_city_bypid/{}'.format(pd['id'])
            yield scrapy.Request(next_page, callback=self.parse_city, method='POST',
                                 headers=self.headers, body='dealer_type=dot_query&ajax=true',
                                 cb_kwargs=dict(province=pd))

    def parse_city(self, response, province):
        for c in response.xpath('//option')[1:]:
            cd = {
                'id':c.xpath('./@city_id').get(),
                'name': c.xpath('./@value').get(),
            }
            # print(cd)
            post_data = 'dealer_flag=dot_query&ajax=1&city={}'.format(cd['name'])
            next_page = 'http://www.dongfeng-honda.com/index.php/Index/get_dealer_by_city'
            yield scrapy.Request(next_page, callback=self.parse_dlr, method='POST',
                                 headers=self.headers, body=post_data,
                                 cb_kwargs=dict(province=province, city=cd))

    def parse_dlr(self, response, province, city):
        dlrs = json.loads(response.text)
        for dlr in dlrs['data']:
            dealer = {
                '编号': self.count,
                '省份': province['name'],
                '城市': city['name'],
                '县区': '',
                '品牌': self.name,
                '公司名称': dlr['dealer_name'],
                '联系电话': dlr['dealer_fwtel'],
                '地址': dlr['dealer_address'],
                '经度': dlr['dealer_lon'],
                '纬度': dlr['dealer_lat'],
                '坐标': '{}, {}'.format(dlr['dealer_lon'], dlr['dealer_lat']),
                'crawlTime': datetime.today(),
                }
            self.count += 1
            yield dealer

