# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
import json
import requests


class HyundaiSpider(scrapy.Spider):
    name = 'hyundai'
    allowed_domains = ['beijing-hyundai.com.cn']
    start_urls = ['https://www.beijing-hyundai.com.cn/umbraco/surface/Common/GetDealers?tag=']

    def parse(self, response):
        pr = requests.get('https://www.beijing-hyundai.com.cn/umbraco/surface/Common/GetProvinces', verify=False)
        cr = requests.get('https://www.beijing-hyundai.com.cn/umbraco/surface/Common/GetCitys', verify=False)
        province = json.loads(pr.text)
        city = json.loads(cr.text)
        pd = {}
        cd = {}
        for i in province['Data']:
            pd[i['ProvinceId']] = i['ProvinceName']
        for i in city['Data']:
            cd[i['CityId']] = i['CityName']

        dlrs = json.loads(response.text)
        for dlr in dlrs['Data']:
            dealer = {
                '编号': dlr['DealerCode'],
                '省份': pd[dlr['ProvinceId']],
                '城市': cd[dlr['CityId']],
                '县区': '',
                '品牌' : self.name,
                '公司名称':dlr['DealerName'],
                '联系电话':dlr['Tel'],
                '地址':dlr['Address'],
                '经度':dlr['Lng'],
                '纬度':dlr['Lat'],
                '坐标':dlr['Lng']+','+dlr['Lat'],
                'crawlTime': datetime.today(),
            }
            yield dealer