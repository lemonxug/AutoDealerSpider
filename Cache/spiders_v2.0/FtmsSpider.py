# coding=utf-8
import json
import pandas as pd
from DemoSpider import DemoSpider
import requests

name = '一汽丰田'
url = 'https://www.ftms.com.cn/website/Maintenance/getProvince'  # 一汽丰田


class FtmsSpider(DemoSpider):


    def __init__(self):
        self.url = url
        self.name = name

    def prase_response(self, r):
        '''
        https://www.ftms.com.cn/website/Maintenance/getProvince
        https://www.ftms.com.cn/website/Maintenance/getCity?cid=110000
        https://www.ftms.com.cn/website/Dealer/getDealer
        '''
        try:
            print('正在处理'+self.name+'经销商信息。。。')
            dlr_list = []
            province = json.loads(bytes.decode(r.content))
            for province in province['data']:
                # print(province)
                r = requests.get('https://www.ftms.com.cn/website/Maintenance/getCity?cid=' + province['cid'])
                for city in json.loads(bytes.decode(r.content))['data']:
                    # print(city)
                    post_data = {"cityid": city['cid'],"cityName": "",
                                 "dealerName": "", "provinceid":  province['cid'], "provinceName": ""}
                    r = requests.post('https://www.ftms.com.cn/website/Dealer/getDealer' , data=json.dumps(post_data))
                    print(r.url)
                    print(post_data)
                    for dlr in json.loads(bytes.decode(r.content))['data']['list']:
                        # print(dlr)
                        dealer = {
                            '编号': dlr['id'],
                            '省份': dlr['province'],
                            '城市': dlr['city'],
                            '县区': '',
                            '品牌' : self.name,
                            '公司名称':dlr['fullname'],
                            '联系电话':dlr['phone_seal'],
                            '地址':dlr['address'],
                            '经度':dlr['lng'],
                            '纬度':dlr['lat'],
                            '坐标':dlr['lng']+','+dlr['lat'],
                            '分类':'',
                        }
                        print(dealer)
                        dlr_list.append(dealer)

            dlrs = pd.DataFrame(dlr_list)
            self.dlrs = dlrs[['编号','省份','城市','县区','品牌','公司名称','联系电话','地址','经度','纬度','坐标', '分类']]
        except Exception as e:
            raise e


if __name__ == '__main__':
    s = FtmsSpider()
    s.run()
