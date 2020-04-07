# coding=utf-8
import json
import pandas as pd
from DemoSpider import DemoSpider


name = 'DS'
url = 'http://www.ds.com.cn/web/cn/api/dealers?lang=cn&type=3'


class DsSpider(DemoSpider):


    def __init__(self):
        self.url = url
        self.name = name

    def prase_response(self, r):
        try:
            print('正在处理'+self.name+'经销商信息。。。')
            data = json.loads(bytes.decode(r.content))
            areas =  data['arealist']

            def extract_city(area, code):
                p_code = code[:2] + '0000'
                P_name = area[p_code]['AreaName']
                c_name = area[p_code]['city'][code]['AreaName']
                return P_name, c_name

            dlrs = data['dealers']
            dlr_list = []
            for dlr in dlrs:
                dealer = {
                    '编号': dlr['code'],
                    '省份': extract_city(areas, dlr['city'])[0],
                    '城市': extract_city(areas, dlr['city'])[1],
                    '县区': '',
                    '品牌' : self.name,
                    '公司名称':dlr['fullname'].split()[0],
                    '联系电话':dlr['selltel'],
                    '地址':dlr['address'],
                    '经度':dlr['lon'],
                    '纬度':dlr['lat'],
                    '坐标':dlr['lon']+','+dlr['lat'],
                    '分类':dlr['store_type'],
                }
                print(dealer)
                dlr_list.append(dealer)

            dlrs = pd.DataFrame(dlr_list)
            self.dlrs = dlrs[['编号','省份','城市','县区','品牌','公司名称','联系电话','地址','经度','纬度','坐标', '分类']]
        except Exception as e:
            raise e


if __name__ == '__main__':
    s = DsSpider()
    s.run()
