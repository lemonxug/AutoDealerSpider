# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
import json
from lxml import etree


class SvmSpider(scrapy.Spider):
    name = 'svm'
    allowed_domains = ['svw-volkswagen.com']
    start_urls = ['http://www.svw-volkswagen.com/']

    def parse(self, response):
        pt = '''
        <option data-v-7a4af686="" value="110000">北京市</option>
        <option data-v-7a4af686="" value="120000">天津市</option>
        <option data-v-7a4af686="" value="130000">河北省</option>
        <option data-v-7a4af686="" value="140000">山西省</option>
        <option data-v-7a4af686="" value="150000">内蒙古自治区</option>
        <option data-v-7a4af686="" value="210000">辽宁省</option>
        <option data-v-7a4af686="" value="220000">吉林省</option>
        <option data-v-7a4af686="" value="230000">黑龙江省</option>
        <option data-v-7a4af686="" value="310000">上海市</option>
        <option data-v-7a4af686="" value="320000">江苏省</option>
        <option data-v-7a4af686="" value="330000">浙江省</option>
        <option data-v-7a4af686="" value="340000">安徽省</option>
        <option data-v-7a4af686="" value="350000">福建省</option>
        <option data-v-7a4af686="" value="360000">江西省</option>
        <option data-v-7a4af686="" value="370000">山东省</option>
        <option data-v-7a4af686="" value="410000">河南省</option>
        <option data-v-7a4af686="" value="420000">湖北省</option>
        <option data-v-7a4af686="" value="430000">湖南省</option>
        <option data-v-7a4af686="" value="440000">广东省</option>
        <option data-v-7a4af686="" value="450000">广西壮族自治区</option>
        <option data-v-7a4af686="" value="460000">海南省</option>
        <option data-v-7a4af686="" value="500000">重庆市</option>
        <option data-v-7a4af686="" value="510000">四川省</option>
        <option data-v-7a4af686="" value="520000">贵州省</option>
        <option data-v-7a4af686="" value="530000">云南省</option>
        <option data-v-7a4af686="" value="540000">西藏自治区</option>
        <option data-v-7a4af686="" value="610000">陕西省</option>
        <option data-v-7a4af686="" value="620000">甘肃省</option>
        <option data-v-7a4af686="" value="630000">青海省</option>
        <option data-v-7a4af686="" value="640000">宁夏回族自治区</option>
        <option data-v-7a4af686="" value="650000">新疆维吾尔自治区</option>
        <option data-v-7a4af686="" value="710000">台湾省</option>
        <option data-v-7a4af686="" value="810000">香港特别行政区</option>
        <option data-v-7a4af686="" value="820000">澳门特别行政区</option>
        '''
        ph = etree.HTML(pt)
        for p in ph.xpath('//option'):
            pd = {
                'id': p.xpath('./@value')[0],
                'name': p.xpath('./text()')[0],
            }
            next_page = 'https://brand.svw-volkswagen.com/api?perPage=500&action=SearchDealers&' \
                        'regionCode={}&dealerType=F&type=toproduct'.format(pd['id'])
            yield scrapy.Request(next_page, callback=self.parse_dlr)

    def parse_dlr(self, response):
        data = json.loads(response.text)
        dlrs = json.loads(data['ReturnValue'])
        for dlr in dlrs['data']:
            dealer = {
                '编号': dlr['orgCode'],
                '省份': dlr['province'],
                '城市': dlr['city'],
                '县区': dlr['region'],
                '品牌': self.name,
                '公司名称': dlr['orgName'],
                '联系电话': dlr['salesPhone'],
                '地址': dlr['address'],
                '经度': dlr['lbsLongitude'],
                '纬度': dlr['lbsLatitude'],
                '坐标': '{}, {}'.format(dlr['lbsLongitude'], dlr['lbsLatitude']),
                'crawlTime': datetime.today(),
            }
            yield dealer