# coding=utf-8
import json
import requests
from datetime import *
import pandas as pd
from DemoSpider import DemoSpider


today = date.strftime(date.today(), '%Y%m%d')
name = '北京现代'
url = 'https://www.beijing-hyundai.com.cn/datacenter/static/js/District.js'


class HyundaiSpider(DemoSpider):

    def __init__(self):
        self.url = url
        self.name = name


    def prase_response(self, r):
        try:
            print('正在处理'+self.name+'经销商信息。。。')
            dlr_dict = {}
            s = bytes.decode(r.content).replace(u'\xa0', u'')[35:]
            for item in s.split(';District'):
                try:
                    key = item[1:6]
                    value = item[8:]
                    dlr = json.loads(value)
                    dlr_dict[key] = dlr
                except:
                    key = item[1:6]
                    value = item[8:-1]
                    dlr = json.loads(value)
                    dlr_dict[key] = dlr
            dlr_list = []
            for dlr in dlr_dict.values():
                dealer = {
                    '编号': dlr['DealerSN'],
                    '省份': '',
                    '城市': dlr['CityID'],
                    '县区': '',
                    '品牌': self.name,
                    '公司名称': dlr['DisName'],
                    '联系电话': dlr['Tel'],
                    '地址': dlr['Address'].replace(u'\xa0', ''),
                    '经度': dlr['Lng'],
                    '纬度': dlr['Lat'],
                    '坐标': dlr['Lng'] + ',' + dlr['Lat'],
                    '分类': dlr['DisSort'] ,
                }
                dlr_list.append(dealer)
            dlrs = pd.DataFrame(dlr_list)

            self.dlrs = dlrs[['编号','省份','城市','县区','品牌','公司名称','联系电话','地址','经度','纬度','坐标', '分类']]
        except Exception as e:
            print(e)


if __name__ == '__main__':
    s = HyundaiSpider()
    s.run()
