# coding=utf-8
import json
import pandas as pd
from DemoSpider import DemoSpider
import requests
from bs4 import BeautifulSoup


name = '广汽丰田'
url = 'https://www.gac-toyota.com.cn/js/newprovincecitydealer/data/provinceData.js'  # 广汽丰田


class GactoyotaSpider(DemoSpider):


    def __init__(self):
        self.url = url
        self.name = name

    def prase_response(self, r):
        # 改动
        '''
        https://www.gac-toyota.com.cn/js/newprovincecitydealer/data/provinceData.js
        https://www.gac-toyota.com.cn/js/newprovincecitydealer/data/cityData.js
        https://www.gac-toyota.com.cn/js/newprovincecitydealer/data/dealerData.js
        '''
        try:
            print('正在处理'+self.name+'经销商信息。。。')
            dlr_list = []

            def to_dict(data):
                t_dict = {}
                for i in data:
                    t_dict[i['value']] = i
                return  t_dict
            # print(bytes.decode(r.content)[20:])
            province = json.loads(bytes.decode(r.content)[20:])
            print(province)
            r = requests.get('https://www.gac-toyota.com.cn/js/newprovincecitydealer/data/cityData.js')
            city = json.loads(bytes.decode(r.content)[16:])
            province_dict = to_dict(province)
            city_dict = to_dict(city)

            r = requests.get('https://www.gac-toyota.com.cn/js/newprovincecitydealer/data/dealerData.js')
            dlrs = json.loads(bytes.decode(r.content)[18:])

            for dlr in dlrs:
                # print(dlr)
                dealer = {
                    '编号': dlr['DealerCode'],
                    '省份': province_dict[city_dict[dlr['City']]['parent']]['name'],
                    '城市': city_dict[dlr['City']]['name'],
                    '县区': '',
                    '品牌' : self.name,
                    '公司名称':dlr['DealerName'],
                    '联系电话':dlr['Tel'],
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
    s = GactoyotaSpider()
    s.run()
