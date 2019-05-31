# coding=utf-8
import json
import pandas as pd
from DemoSpider import DemoSpider
from bs4 import BeautifulSoup
import requests


name = '东风雪铁龙'
url = 'http://www.dongfeng-citroen.com.cn/4s/index.php/dsearch'  # 东风雪铁龙


class DfcitroenSpider(DemoSpider):


    def __init__(self):
        self.url = url
        self.name = name

    def prase_response(self, r):
        try:
            print('正在处理'+self.name+'经销商信息。。。')
            dlr_list = []
            soup = BeautifulSoup(r.content, 'lxml')

            def has_dataid_but_no_class(tag):
                return tag.has_attr('data-id') and not tag.has_attr('class')

            province_dict = {}
            for li in soup.find_all(has_dataid_but_no_class):
                province = {}
                key = li['data-id']
                value = li.string
                province['id'] = key
                province['name'] = value
                province_dict[key] = province
            # print(province_dict)
            city_dict = {}
            for k in province_dict.keys():
                r = requests.get('http://www.dongfeng-citroen.com.cn/4s/index.php/api/getCities/' + k)
                # print(r.content)
                for city in json.loads(bytes.decode(r.content)):
                    key = city['id']
                    value = city
                    city_dict[key] = value
            # print(city_dict)
            for k in city_dict.keys():
                r = requests.post('http://www.dongfeng-citroen.com.cn/4s/index.php/api/getDealersByLocation?', data={
                    'city': k})
                # print(r.content)
                for dlr in json.loads(bytes.decode(r.content))['list']:
                    dealer = {
                        '编号': dlr['dealer_code'],
                        '省份': province_dict[dlr['province']]['name'],
                        '城市': city_dict[dlr['city']]['city'],
                        '县区': '',
                        '品牌' : self.name,
                        '公司名称':dlr['dealer_name'],
                        '联系电话':dlr['sale_tel'],
                        '地址':dlr['address'],
                        '经度':dlr['x'],
                        '纬度':dlr['y'],
                        '坐标':dlr['x']+','+dlr['y'],
                        '分类':'',
                    }
                    print(dealer)
                    dlr_list.append(dealer)

            dlrs = pd.DataFrame(dlr_list)
            self.dlrs = dlrs[['编号','省份','城市','县区','品牌','公司名称','联系电话','地址','经度','纬度','坐标', '分类']]
        except Exception as e:
            raise e


if __name__ == '__main__':
    s = DfcitroenSpider()
    s.run()
