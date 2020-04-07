# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
import json


class NissanSpider(scrapy.Spider):
    name = 'nissan'
    allowed_domains = ['dongfeng-nissan.com.cn']
    start_urls = ['http://dongfeng-nissan.com.cn/']

    def parse(self, response):
        provinces = [{ "id": 1, "name": "北京" },
                     { "id": 2, "name": "天津" },
                     { "id": 3, "name": "河北" },
                     { "id": 4, "name": "山西" },
                     { "id": 5, "name": "内蒙古" },
                     { "id": 6, "name": "辽宁" },
                     { "id": 7, "name": "吉林" },
                     { "id": 8, "name": "黑龙江" },
                     { "id": 9, "name": "上海" },
                     { "id": 10, "name": "江苏" },
                     { "id": 11, "name": "浙江" },
                     { "id": 12, "name": "安徽" },
                     { "id": 13, "name": "福建" },
                     { "id": 14, "name": "江西" },
                     { "id": 15, "name": "山东" },
                     { "id": 16, "name": "河南" },
                     { "id": 17, "name": "湖北" },
                     { "id": 18, "name": "湖南" },
                     { "id": 19, "name": "广东" },
                     { "id": 20, "name": "广西" },
                     { "id": 21, "name": "海南" },
                     { "id": 22, "name": "重庆" },
                     { "id": 23, "name": "四川" },
                     { "id": 24, "name": "贵州" },
                     { "id": 25, "name": "云南" },
                     { "id": 26, "name": "西藏" },
                     { "id": 27, "name": "陕西" },
                     { "id": 28, "name": "甘肃" },
                     { "id": 29, "name": "青海" },
                     { "id": 30, "name": "宁夏" },
                     { "id": 31, "name": "新疆" }]
        for p in provinces:
            next_page = 'https://api.dongfeng-nissan.com.cn/api/Nissan/GetNissanCity'
            post_data = {'provinceId': '{}'.format(p['id'])}
            yield scrapy.FormRequest(next_page, callback=self.parse_city,
                                     formdata=post_data,
                                     cb_kwargs=dict(province=p))
    def parse_city(self, response, province):
        citys = json.loads(response.text)
        for c in citys['data']['CityInfoList']:
            next_page = 'https://www.dongfeng-nissan.com.cn/Nissan/ajax/Distributor/GetJsonDistributorList'
            post_data = {'storeName': '',
                        'province': '{}'.format(province['name']),
                        'cprovince': '江苏省',
                        'city': '{}'.format(c['Name']),
                        'cID': '',
                        'carSeriesId': '',
                        'terminal': '0'}
            yield scrapy.FormRequest(next_page, callback=self.parse_dlr,
                                     formdata=post_data,
                                     cb_kwargs=dict(province=province, city=c))

    def parse_dlr(self, response, province, city):
        dlrs = json.loads(response.text)
        for dlr in dlrs['data']['DealerInfos']:
            dealer = {
                '编号': dlr['StoreID'],
                '省份': province['name'],
                '城市': city['Name'],
                '县区': dlr['District'],
                '品牌': self.name,
                '公司名称': dlr['StoreName'],
                '联系电话': dlr['SaleTel'],
                '地址': '{}{}{}{}'.format(province['name'], city['Name'], dlr['District'], dlr['Address']),
                '经度': dlr['Longitude'],
                '纬度': dlr['Latitude'],
                '坐标': dlr['Longitude']+','+dlr['Latitude'],
                'crawlTime': datetime.today(),
                    }
            yield dealer