# coding=utf-8
import json
import pandas as pd
from DemoSpider import DemoSpider
import xml.etree.ElementTree as ET



name = '上汽大众'
url = 'http://club.svw-volkswagen.com/map/latlng.xml'


class SvmSpider(DemoSpider):


    def __init__(self):
        self.url = url
        self.name = name

    def prase_response(self, r):
        try:
            print('正在处理'+self.name+'经销商信息。。。')
            with open('svm.xml', 'wb') as f:
                f.write(r.content)
            tree = ET.parse('svm.xml')
            root = tree.getroot()
            dlr_list = []
            for area in root:
                for province in area:
                    for city in province:
                        for district in city:
                            for dlr in district:
                                dealer = {
                                    '编号': dlr.attrib['code'],
                                    '省份': province.attrib['name'],
                                    '城市': city.attrib['name'],
                                    '县区': district.attrib['name'],
                                    '品牌' : self.name,
                                    '公司名称':dlr.attrib['name'],
                                    '联系电话':dlr.attrib['tel24'],
                                    '地址':dlr.attrib['address'],
                                    '经度':dlr.attrib['lng'],
                                    '纬度':dlr.attrib['lat'],
                                    '坐标':dlr.attrib['lng']+','+dlr.attrib['lat'],
                                    '分类':dlr.attrib['type'],
                                }
                                print(dealer)
                                dlr_list.append(dealer)

            dlrs = pd.DataFrame(dlr_list)
            self.dlrs = dlrs[['编号','省份','城市','县区','品牌','公司名称','联系电话','地址','经度','纬度','坐标', '分类']]
        except Exception as e:
            raise e


if __name__ == '__main__':
    s = SvmSpider()
    s.run()
