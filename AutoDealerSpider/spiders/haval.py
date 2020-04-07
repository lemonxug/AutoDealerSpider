# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
import json
from urllib import parse


class HavalSpider(scrapy.Spider):
    name = 'haval'
    allowed_domains = ['haval.cn', 'mall.haval.com.cn']
    start_urls = ['https://mall.haval.com.cn/dealerpc.html']
    headers = {
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie':'TC_EV_DIR=9001609da908ceebf496e9919b8132d1; '
             'JSESSIONID=FB70523B53D1967658613324D367CA5E; '
             'Hm_lvt_ed2c87f44fac6742a5d95c11d89dd0a5=1585813343; '
             'Hm_lpvt_ed2c87f44fac6742a5d95c11d89dd0a5=1585813343;'
             ' _gscu_293425980=85813365odplg014; _gscbrs_293425980=1; '
             'Hm_lvt_503e901520f869597c8cba6f4c3efa32=1585813365,1585813381,1585816232;'
             ' Hm_lpvt_503e901520f869597c8cba6f4c3efa32=1585816232;'
             ' _gscs_293425980=85813365zg1u0y14|pv:3; '
             'userSelectedlocation=%7B%22provinceName%22%3A%22%E7%A6%8F%E5%BB%BA%22%2C%22'
             'cityName%22%3A%22%E5%8D%97%E5%B9%B3%22%7D; '
             'SERVERID=a437900730f5c217637a79f63f95333a|1585816238|1585813342; '
             'userLocationId=%7B%22provinceId%22%3A14%2C%22cityId%22%3A154%7D',
            'X-CSRF-TOKEN':'4594ccef2fdb26a47680b9e2a97a2e6b;lky0JC',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/'
                          '537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
            }

    def parse(self, response):
        for c in response.xpath('//div[@id="dealer_areaContainer"]//a'):
            p = c.xpath('./@onclick').re(r"\'(\w*)\'")[0]
            c = c.xpath('./@onclick').re(r"\'(\w*)\'")[1]
            params =  parse.urlencode({'province':p,'city':c})
            params = '%25'.join(params.split('%'))
            next_page = 'https://mall.haval.com.cn/area/returnPlaceId.html?{}'.format(params)
            # print(next_page)
            yield scrapy.Request(next_page, callback=self.parse_city, headers=self.headers)

    def parse_city(self, response):
        cid = response.xpath('//text()').re(':(\d*)')[1]
        next_page = 'https://mall.haval.com.cn/cars/getDealerByType.html'
        # post_data = {'cityId': cid}
        yield scrapy.Request(next_page, callback=self.parse_dlr, method='POST',
                             headers=self.headers, body='cityId={}'.format(cid),)

    def parse_dlr(self, response):
        dlrs = json.loads(response.text)
        for dlr in dlrs['list']:
            dealer = {
                '编号': dlr['storeId'],
                '省份': dlr['province'],
                '城市': dlr['city'],
                '县区': '',
                '品牌': self.name,
                '公司名称': dlr['storeName'],
                '联系电话': dlr['salePhone'],
                '地址': dlr['fullAddress'],
                '经度': dlr['jingWeiDu'].split(',')[0],
                '纬度': dlr['jingWeiDu'].split(',')[1],
                '坐标': dlr['jingWeiDu'],
                'crawlTime': datetime.today(),
            }
            yield dealer