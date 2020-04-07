# coding=utf-8
import json
import pandas as pd
from DemoSpider import DemoSpider
import re
import requests


name = '斯柯达'
url = 'http://www.skoda.com.cn/assets/js/apps/dealerdata.js'  # 斯柯达


class SkodaSpider(DemoSpider):


    def __init__(self):
        self.url = url
        self.name = name

    def prase_request(self, url):
        try:
            print('正在抓取'+self.name+'经销商信息。。。')
            r = requests.get(url, verify=False)
        except Exception as e:
            print('【无法下载网页】')
            raise e
        return r

    def prase_response(self, r):
        try:
            print('正在处理'+self.name+'经销商信息。。。')
            dlr_list = []
            data = bytes.decode(r.content)
            p1 = re.compile('window.DEALERS_DATA.\w* = ')
            m1 = p1.split(data)
            # rssc : 分销中心\r\nprovince : 省份\r\ncity : 城市\r\ndistrict : 区县\r\ndealer : 经销商
            rssc = json.loads(m1[1].strip()[:-1])
            province = json.loads(m1[2].strip()[:-1])
            city = json.loads(m1[3].strip()[:-1])
            # district = json.loads(m1[4].strip()[:-1])
            dealer = json.loads(m1[5].strip()[:-1])
            xy = json.loads(m1[6].split(';')[0])
            # print(m1[6].split(';')[1][22:])
            # xy = json.loads(m1[6].split(';')[1][22:])
            # print(xy)
            def to_dict(columns, values):
                t_dict = {}
                for item in values:
                    tmp = {}
                    for x, y in zip(columns, item):
                        tmp[x] = y
                    t_dict[tmp['code']] = tmp
                    # print(t_dict)
                return t_dict

            province_dict = to_dict(province['columnNames'], province['data'])
            city_dict = to_dict(city['columnNames'], city['data'])
            dealer_dict = to_dict(dealer['columnNames'], dealer['data'])

            for dlr in dealer_dict.values():
                dealer = {
                    '编号': dlr['code'],
                    '省份': province_dict[dlr['province_code']]['name'],
                    '城市': city_dict[dlr['city_code']]['name'],
                    '县区': '',
                    '品牌' : self.name,
                    '公司名称':dlr['name'],
                    '联系电话':dlr['phone'],
                    '地址':dlr['address'],
                    '经度': xy[dlr['code']][1].split(',')[0] if dlr['code'] in xy.keys()  else '',
                    '纬度': xy[dlr['code']][1].split(',')[1] if dlr['code'] in xy.keys()  else '',
                    '坐标': xy[dlr['code']][1] if dlr['code'] in xy.keys()  else '',
                    # '经度':xy['766'+dlr['code']][0].split(',')[0],
                    # '纬度':xy['766'+dlr['code']][0].split(',')[1],
                    # '坐标':xy['766'+dlr['code']][0],
                    '分类':'',
                }
                print(dealer)
                dlr_list.append(dealer)

            dlrs = pd.DataFrame(dlr_list)
            self.dlrs = dlrs[['编号','省份','城市','县区','品牌','公司名称','联系电话','地址','经度','纬度','坐标', '分类']]
        except Exception as e:
            raise e


if __name__ == '__main__':
    s = SkodaSpider()
    s.run()
