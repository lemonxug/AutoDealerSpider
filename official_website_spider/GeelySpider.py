# coding=utf-8
import json
import pandas as pd
from DemoSpider import DemoSpider
import requests
from bs4 import BeautifulSoup


name = '吉利汽车'
url = 'https://www.geely.com/api/geely/official/get/getprovincelist'  # 吉利汽车


class GeelySpider(DemoSpider):


    def __init__(self):
        self.url = url
        self.name = name

    def prase_request(self, url):
        try:
            print('正在抓取'+self.name+'经销商信息。。。')
            header = {
                'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; ZoomSpider.net bot; .NET CLR 1.1.4322)',
                'Referer': 'ttps://www.geely.com',
            }
            r = requests.get(url, headers=header)
        except Exception as e:
            print('【无法下载网页】')
            raise e
        return r

    def prase_response(self, r):
        '''
        https://www.geely.com/api/geely/official/get/getprovincelist
        https://www.geely.com/api/geely/official/get/getcitylist?provinceid=10
        https://www.geely.com/api/geely/official/get/GetDealer?seriesCode=&province=10&city=100004&keyword=
        '''
        try:
            print('正在处理'+self.name+'经销商信息。。。')
            dlr_list = []
            # print(r.status_code)
            # print(r.json())
            provinces = r.json()
            for p in provinces:
                r = self.prase_request('https://www.geely.com/api/geely/official/get/getcitylist?provinceid='+p['regionId'])
                citys = r.json()
                for c in citys:
                    r = self.prase_request('https://www.geely.com/api/geely/official/get/GetDealer?seriesCode=&province='+
                                     p['regionId']+'&city='+c['regionId']+'&keyword=')
                    dealers = r.json()
                    for dlr in dealers:
                        if dlr['dealerId'] == 16180:
                            dlr['coordinates'] = '116.376747,40.018948'
                        dealer = {
                            '编号': dlr['dealerId'],
                            '省份': p['regionName'],
                            '城市': c['regionName'],
                            '县区': '',
                            '品牌' : self.name,
                            '公司名称':dlr['dealerName'],
                            '联系电话':dlr['bizPhone'],
                            '地址':dlr['address'],
                            '经度':dlr['coordinates'][:11] if dlr['coordinates'] else '',
                            '纬度':dlr['coordinates'][11:] if dlr['coordinates'] else '',
                            '坐标':dlr['coordinates'],
                            '分类':'',
                        }
                        print(dealer)
                        dlr_list.append(dealer)

            dlrs = pd.DataFrame(dlr_list)
            self.dlrs = dlrs[['编号','省份','城市','县区','品牌','公司名称','联系电话','地址','经度','纬度','坐标', '分类']]
        except Exception as e:
            raise e


if __name__ == '__main__':
    s = GeelySpider()
    s.run()
