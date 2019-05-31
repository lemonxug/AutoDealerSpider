# coding=utf-8
import json
import pandas as pd
from DemoSpider import DemoSpider
import requests
import re


url = 'https://www.dongfeng-nissan.com.cn/Areas/Nissan/Content/static/src/script/common.js'   #  东风日产
name = '东风日产'


class NissanSpider(DemoSpider):


    def __init__(self):
        self.url = url
        self.name = name

    def prase_response(self, r):
        # https://www.dongfeng-nissan.com.cn/buy/find-dealer
        # https://www.dongfeng-nissan.com.cn/Nissan/ajax/Distributor/GetJsonDistributorList
        try:
            print('正在处理'+self.name+'经销商信息。。。')
            dlr_list = []
            data = bytes.decode(r.content).split('$Json.cityList = ')[1]
            cityList = json.loads(data.split(';')[0])
            # print(cityList)
            for p in cityList:
                # print(p)
                for c in p['child']:
                    post_data = {
                        'storeName' : '',
                        'province' : p['name'],
                        'cprovince' : '江苏省',
                        'city' : c['name'],
                        'cID' : '',
                        'carSeriesId':'',
                        'terminal' : 0,
                    }
                    r = requests.post('https://www.dongfeng-nissan.com.cn/Nissan/ajax/Distributor/GetJsonDistributorList',
                    data=post_data)
                    for dlr in json.loads(bytes.decode(r.content))['data']['DealerInfos']:
                        # print(dlr)
                        dealer = {
                            '编号': dlr['StoreID'],
                            '省份': p['name'],
                            '城市': c['name'],
                            '县区': '',
                            '品牌' : self.name,
                            '公司名称':dlr['StoreName'],
                            '联系电话':dlr['SaleTel'],
                            '地址':dlr['Address'],
                            '经度':dlr['Longitude'],
                            '纬度':dlr['Latitude'],
                            '坐标':dlr['Longitude']+','+dlr['Latitude'],
                            '分类':'',
                        }
                        print(dealer)
                        dlr_list.append(dealer)

            dlrs = pd.DataFrame(dlr_list)
            self.dlrs = dlrs[['编号','省份','城市','县区','品牌','公司名称','联系电话','地址','经度','纬度','坐标', '分类']]
        except Exception as e:
            raise e


if __name__ == '__main__':
    s = NissanSpider()
    s.run()
