# coding=utf-8
import json
from datetime import *
import pandas as pd
from DemoSpider import DemoSpider


name = '一汽大众'
url = 'http://contact.faw-vw.com/uploadfiles/js/dealer.js'


class FawvmSpider(DemoSpider):


    def __init__(self):
        self.url = url
        self.name = name

    def prase_response(self, r):
        try:
            print('正在处理'+self.name+'经销商信息。。。')
            s = bytes.decode(r.content).replace(u'\xa0', '')[16:]
            dlrs = json.loads(s)
            dlr_list = []
            for dlr in dlrs:
                dealer = {
                    '编号': dlr['vd_dealerCode'],
                    '省份': dlr['vp_name'].split()[1],
                    '城市': dlr['vc_name'],
                    '县区': '',
                    '品牌' : self.name,
                    '公司名称':dlr['vd_dealerName'],
                    '联系电话':dlr['vd_salePhone'],
                    '地址':dlr['vd_address'],
                    '经度':dlr['vd_longitude'],
                    '纬度':dlr['vd_latitude'],
                    '坐标':dlr['vd_longitude']+','+dlr['vd_latitude'],
                    '分类':dlr['vd_dealerType'],
                }
                print(dealer)
                dlr_list.append(dealer)

            dlrs = pd.DataFrame(dlr_list)
            self.dlrs = dlrs[['编号','省份','城市','县区','品牌','公司名称','联系电话','地址','经度','纬度','坐标', '分类']]
        except Exception as e:
            raise e


if __name__ == '__main__':
    s = FawvmSpider()
    s.run()
