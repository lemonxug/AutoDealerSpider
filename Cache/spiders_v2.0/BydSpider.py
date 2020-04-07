# coding=utf-8
import json
import pandas as pd
from DemoSpider import DemoSpider
import requests
from bs4 import BeautifulSoup


name = '比亚迪'
url = 'http://www.bydauto.com.cn/counter-sellpoint.html'  # 比亚迪


class BydSpider(DemoSpider):


    def __init__(self):
        self.url = url
        self.name = name

    def prase_response(self, r):
        try:
            print('正在处理'+self.name+'经销商信息。。。')
            dlr_list = []
            soup = BeautifulSoup(r.content, 'lxml')
            car_dict = {}
            for op in soup.find(id='carid'):
                car = {}
                if op.string != '\n':
                    if op['value'] != '0':
                        key = op['value']
                        car['id'] = key
                        car['name'] = op.string
                        car_dict[key] = car
            for k in car_dict.keys():
                postdata = {'carid': k}
                r = requests.post('http://www.bydauto.com.cn/ajax.php?act=getpro&inajax=1', data=postdata)
                soup = BeautifulSoup(r.content, 'lxml')
                for op1 in soup.find_all('option'):
                    postdata = {'pid': op1.string, 'carid': k}
                    r = requests.post('http://www.bydauto.com.cn/ajax.php?act=getcity&inajax=1', data=postdata)
                    soup = BeautifulSoup(r.content, 'lxml')
                    try:
                        for op2 in soup.find_all('option'):
                            postdata = {'showtype': 'json', 'cid': op2.string, 'carid': k}
                            r = requests.post('http://www.bydauto.com.cn/ajax.php?act=getsellpoint&inajax=1',
                                              data=postdata)
                            for dlr in json.loads(bytes.decode(r.content)):
                                # print(dlr)
                                dealer = {
                                    '编号': dlr['id'],
                                    '省份': op1.string,
                                    '城市': op2.string,
                                    '县区': '',
                                    '品牌': self.name,
                                    '公司名称': dlr['sjname'],
                                    '联系电话': dlr['phone'],
                                    '地址': dlr['address'],
                                    '经度': dlr['jingdu'],
                                    '纬度': dlr['weidu'],
                                    '坐标': dlr['jingdu'] + ',' + dlr['weidu'],
                                    '分类': '',
                                }
                                print(dealer)
                                dlr_list.append(dealer)
                    except:
                        print(k, op1.string)

            dlrs = pd.DataFrame(dlr_list)
            self.dlrs = dlrs[['编号','省份','城市','县区','品牌','公司名称','联系电话','地址','经度','纬度','坐标', '分类']]
        except Exception as e:
            raise e


if __name__ == '__main__':
    s = BydSpider()
    s.run()
