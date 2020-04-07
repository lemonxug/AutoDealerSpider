# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
import json


class FordSpider(scrapy.Spider):
    name = 'ford'
    allowed_domains = ['ford.com.cn', 'amap.com']
    start_urls = ['https://www.ford.com.cn/content/ford/cn/zh_cn/configuration/application-and-services-config/provinceCityDropDowns.multiFieldDropdownChina.data']

    def parse(self, response):
        for p in json.loads(response.text):
            for c in p['cityList']:
                next_page = 'https://restapi.amap.com/v3/geocode/geo?' \
                            'key=1891d0f847c0a210a88015fdd4c3bc46&s=rsv3&callback=jsonp_232&' \
                            'platform=JS&logversion=2.0&sdkversion=1.3&' \
                            'appname=http://www.ford.com.cn/dealer/locator?' \
                            'intcmp=hp-return-fd&csid=D6C889F7-2FF1-4EA5-8D60-494D42872518&' \
                            'address={}'.format(p['provinceKey']+c['cityKey'])
                yield scrapy.Request(next_page, callback=self.parse_city,
                                     cb_kwargs=dict(p=p['provinceKey'], c=c['cityKey']))

    def parse_city(self, response, p, c):
        cr = json.loads(response.text[10:-1])
        next_page = 'https://yuntuapi.amap.com/datasearch/local?' \
              's=rsv3&key=1891d0f847c0a210a88015fdd4c3bc46&extensions=all&' \
              'language=en&enc=utf-8&output=jsonp&&sortrule=_distance:1&' \
              'autoFitView=true&panel=result&keywords=&limit=100&sortrule=_id:1&' \
              'tableid=55adb0c7e4b0a76fce4c8dd6&radius=50000&platform=JS&' \
              'logversion=2.0&sdkversion=1.4.2&appname=http://www.ford.com.cn/dealer/locator?' \
              'intcmp=hp-return-fd&csid=6F094767-5285-454B-BC73-0D18F9C7223B&' \
              'center={}&city={}&filter=AdministrativeArea:{}&callback=jsonp_333'.format(
                cr['geocodes'][0]['location'], c, p)
        yield scrapy.Request(next_page, callback=self.parse_dlr)

    def parse_dlr(self, response):
        dlrs = json.loads(response.text[10:-1])
        for dlr in dlrs['datas']:
            dealer = {
                '编号': dlr['_id'],
                '省份': dlr['_province'],
                '城市': dlr['_city'],
                '县区': dlr['_district'],
                '品牌': self.name,
                '公司名称': dlr['_name'],
                '联系电话': dlr['ServicePhoneNumber'],
                '地址': dlr['_address'],
                '经度': dlr['_location'].split(',')[0],
                '纬度': dlr['_location'].split(',')[1],
                '坐标': dlr['_location'],
                'crawlTime': datetime.today(),
            }
            yield dealer
