# coding=utf-8
import json
import requests
from datetime import *
import pandas as pd
from DemoSpider import DemoSpider


today = date.strftime(date.today() , '%Y%m%d')
name = '东风悦达起亚'
url = 'http://www.dyk.com.cn/public/dyk/js/allDealersData.js'

class DykmcSpider(DemoSpider):

    def __init__(self):
        self.url = url
        self.name = name

    def prase_response(self, r):
        try:
            print('正在处理'+self.name+'经销商信息。。。')
            dlr_dict = json.loads(bytes.decode(r.content)[18:])  # bytes to string, string to dict
            dlr_list = []
            for keys, values in dlr_dict.items():
                for dlr in values:
                    dealer = {
                        '编号': dlr['经销商代码'],
                        '省份': dlr['province_name'],
                        '城市': dlr['city_name'],
                        '县区': dlr['district_name'],
                        '品牌' : self.name,
                        '公司名称':dlr['name'],
                        '联系电话':dlr['sale_phone'],
                        '地址':dlr['address'].replace(u'\xa0', ''),
                        '经度':dlr['place'].split(',')[0],
                        '纬度':dlr['place'].split(',')[1],
                        '坐标':dlr['place'],
                        '分类':dlr['类别'],
                    }
                    print(dealer)
                    dlr_list.append(dealer)

            dlrs = pd.DataFrame(dlr_list)
            self.dlrs = dlrs[['编号','省份','城市','县区','品牌','公司名称','联系电话','地址','经度','纬度','坐标', '分类']]
        except Exception as e:
            print(e)



if __name__ == '__main__':
    s = DykmcSpider()
    s.run()
