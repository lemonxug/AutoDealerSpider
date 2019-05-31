# coding=utf-8
import json
import pandas as pd
from DemoSpider import DemoSpider


name = '广汽本田'
url = 'http://www.ghac.cn/js/Official/staticData/p_c_dealers_data.js'  # 广汽本田


class GhacSpider(DemoSpider):


    def __init__(self):
        self.url = url
        self.name = name

    def prase_response(self, r):
        # 改版了
        try:
            print('正在处理'+self.name+'经销商信息。。。')
            dlr_list = []
            province, city, dlr, _, _, _, _, _ = r.content.split(b';')
            province_dict = {}
            city_dict = {}
            for province in json.loads(bytes.decode(province[119:])):
                key = province['PROVINCE_ID']
                value = province
                province_dict[key] = value
            for city in json.loads(bytes.decode(city[24:])):
                key = city['CITY_ID']
                value = city
                city_dict[key] = value
            for dlr in json.loads(bytes.decode(dlr[27:])):
                try:
                    dlr['city'] = city_dict[dlr['CITY_ID']]['CITY_NAME']
                    dlr['province'] = province_dict[city_dict[dlr['CITY_ID']]['PROVINCE_ID']]['PROVINCE_NAME']
                    dealer = {
                        '编号': dlr['DEALER_CODE'],
                        '省份': dlr['province'],
                        '城市': dlr['city'],
                        '县区': '',
                        '品牌': self.name,
                        '公司名称': dlr['REGISTRATION_NAME'],
                        '联系电话': dlr['SALES_PHONE'],
                        '地址': dlr['ADDRESS'],
                        '经度': dlr['LONGITUDE'],
                        '纬度': dlr['LATITUDE'],
                        '坐标': dlr['LONGITUDE'] + ',' + dlr['LATITUDE'],
                        '分类': dlr['DLevel'],
                    }
                    print(dealer)
                    dlr_list.append(dealer)
                except:
                    print('【处理失败】',dlr['CITY_ID'], dlr)
                    continue

            dlrs = pd.DataFrame(dlr_list)
            self.dlrs = dlrs[['编号','省份','城市','县区','品牌','公司名称','联系电话','地址','经度','纬度','坐标', '分类']]
        except Exception as e:
            raise e


if __name__ == '__main__':
    s = GhacSpider()
    s.run()
