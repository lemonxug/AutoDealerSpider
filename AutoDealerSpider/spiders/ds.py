# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime


class DsSpider(scrapy.Spider):
    name = 'ds'
    allowed_domains = ['ds.com.cn']
    start_urls = ['http://ds.com.cn/']

    def parse(self, response):
        pass
