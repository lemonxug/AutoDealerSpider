# coding=utf-8
import json
import pandas as pd
from DemoSpider import DemoSpider


name = '别克'
url = 'http://www.buick.com.cn/api/dealer.aspx'     # 别克


class BuickSpider(DemoSpider):


    def __init__(self):
        self.url = url
        self.name = name

    def prase_response(self, r):
        try:
            print('正在处理'+self.name+'经销商信息。。。')
            dlrs = json.loads(bytes.decode(r.content).replace(u'\xa0', u''))
            dlr_list = []
            for dlr in dlrs:
                dealer = {
                    '编号': dlr['dealerCode'],
                    '省份': dlr['provinceName'],
                    '城市': dlr['cityName'],
                    '县区': dlr['districtName'],
                    '品牌' : self.name,
                    '公司名称':dlr['dealerName'],
                    '联系电话':dlr['tel'],
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
    s = BuickSpider()
    s.run()
