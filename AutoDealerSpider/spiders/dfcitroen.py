# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
import json

class DfcitroenSpider(scrapy.Spider):
    name = 'dfcitroen'
    allowed_domains = ['dongfeng-citroen.com.cn']
    start_urls = ['http://www.dongfeng-citroen.com.cn/4s/index.php/dsearch']

    def parse(self, response):
        for p in response.xpath('//div[@class="H_headercon02"]//li'):
            pname = p.xpath('./text()').get()
            pid = p.xpath('./@data-id').get()
            next_page = 'http://www.dongfeng-citroen.com.cn/4s/index.php/api/getCities/{}'.format(pid)
            yield scrapy.Request(next_page, callback=self.parse_city,
                                 cb_kwargs=dict(province=pname))

    def parse_city(self, response, province):
        citys = json.loads(response.text)
        for c in citys:
            cname = c['city']
            cid = c['id']
            next_page = 'http://www.dongfeng-citroen.com.cn/4s/index.php/api/getDealersByLocation'
            post_data = {'city': cid}
            yield scrapy.FormRequest(next_page, callback=self.parse_dlr, method='POST',
                                 formdata=post_data,
                                 cb_kwargs=dict(province=province, city=cname))

    def parse_dlr(self, response, province, city):
        dlrs = json.loads(response.text)
        for dlr in dlrs['list']:
            dealer = {
                '编号': dlr['dealer_code'],
                '省份': province,
                '城市': city,
                '县区': '',
                '品牌': self.name,
                '公司名称': dlr['dealer_name'],
                '联系电话': dlr['sale_tel'],
                '地址': dlr['address'].replace(u'\xa0', ''),
                '经度': dlr['x'],
                '纬度': dlr['y'],
                '坐标': '{}, {}'.format(dlr['x'], dlr['y']),
                'crawlTime': datetime.today(),
                }
            yield dealer
