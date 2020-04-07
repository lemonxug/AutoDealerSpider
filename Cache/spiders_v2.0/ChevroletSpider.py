# coding=utf-8
import json
import pandas as pd
from DemoSpider import DemoSpider


name = '雪佛兰'
url = 'http://www.mychevy.com.cn/images/files/indexmap.txt'  # 雪佛兰


class ChevroletSpider(DemoSpider):


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
                    '编号': dlr['code'],
                    '省份': dlr['province'],
                    '城市': dlr['city'],
                    '县区': '',
                    '品牌' : self.name,
                    '公司名称':dlr['name'],
                    '联系电话':dlr['tel'],
                    '地址':dlr['address'],
                    '经度':dlr['lng'],
                    '纬度':dlr['lat'],
                    '坐标':dlr['lng']+','+dlr['lat'],
                    '分类':dlr['lever'],
                }
                print(dealer)
                dlr_list.append(dealer)

            dlrs = pd.DataFrame(dlr_list)
            self.dlrs = dlrs[['编号','省份','城市','县区','品牌','公司名称','联系电话','地址','经度','纬度','坐标', '分类']]
        except Exception as e:
            raise e


if __name__ == '__main__':
    s = ChevroletSpider()
    s.run()
