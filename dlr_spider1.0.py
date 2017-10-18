# -*- coding : utf-8 -*-

import json
import csv
import requests
import os
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET   # 解析XML文件
import xml.dom.minidom   # 解析XML文件


class DykmcSpider(object):

    def __init__(self, domain, url):
        self.domain = domain
        self.js_url = url

    def get_data(self):
        if (self.domain + '.json') not in os.listdir(os.getcwd()):
            dlr_dict = self.prase_request()
            if dlr_dict:
                self.save_as_json(dlr_dict)
        #     if self.domain == 'dyk':
        #         r = requests.get(self.js_url)  # post??
        #         dlr_dict = json.loads(bytes.decode(r.content)[18:])  # bytes to string, string to dict
        #         self.save_as_json(dlr_dict)
        #     if self.domain == 'hyundai':
        #         r = requests.get(self.js_url)  # 是get方法！
        #         dlr_dict = {}
        #         s = bytes.decode(r.content)[27:]
        #         for item in s.split(';'):
        #             try:
        #                 key = item[9:14]
        #                 value = item[16:]
        #                 dlr = json.loads(value)
        #                 dlr_dict[key] = dlr
        #             except:
        #                 print(item)
        #         self.save_as_json(dlr_dict)

        else:
            with open(self.domain+'.json', 'r') as f:
                dlr_dict = json.load(f)
        return dlr_dict

    def prase_request(self):
        r = requests.get(self.js_url)  # post??
        dlr_dict = json.loads(bytes.decode(r.content)[18:])  # bytes to string, string to dict
        return dlr_dict

    def prase_data(self):
        dlr_list = []
        data = self.get_data()
        if self.domain == 'dyk':
            for keys, values in data.items():
                for dlr in values:
                    dlr['address'] = dlr['address'].replace(u'\xa0', '')   # '宁夏省银川市金凤区工业集中区创业街西侧\xa0',
                    soup = BeautifulSoup(dlr['dealer_1'], 'lxml')
                    dlr['dealer_1'] = soup.span.string
                    dlr_list.append(dlr)
        else:
            for v in data.values():
                dlr_list.append(v)
        return dlr_list

    def save_as_json(self, data):
        with open(self.domain+'.json', 'w') as f:
            j_dlr_dict = json.dumps(data)   # 转换成字符串
            f.write(j_dlr_dict)    # 写入文件

    def export_data(self):
        data = self.prase_data()
        with open(self.domain+'.csv', 'w', encoding='gbk', newline='') as f:   # newline=''  不再有多余空行
            w = csv.writer(f)
            w.writerow(data[1].keys())
            for item in data:
                try:
                    w.writerow(item.values())  # 报错‘gbk’ 不能编译‘\xao’
                except:
                    print(item.values())   # 打印出报错的数据


class HyundaiSpider(DykmcSpider):

    def prase_request(self):
        r = requests.get(self.js_url)  # 是get方法！
        dlr_dict = {}
        s = bytes.decode(r.content)[27:]
        for item in s.split(';'):
            try:
                key = item[9:14]
                value = item[16:]
                dlr = json.loads(value)
                dlr_dict[key] = dlr
            except:
                print(item)
        return dlr_dict

    def prase_data(self):
        dlr_list = []
        data = self.get_data()
        data['11814']['Tel'] = data['11814']['Tel'].replace(u'\xa0', u'')
        data['11814']['Sales_tel'] = data['11814']['Sales_tel'].replace(u'\xa0', u'')
        for v in data.values():
            dlr_list.append(v)
        return dlr_list


class FawvmSpider(DykmcSpider):

    def prase_request(self):
        r = requests.get(self.js_url)  # 是get方法！
        dlr_dict = {}
        s = bytes.decode(r.content)[16:]
        dlr_list = json.loads(s)
        for item in dlr_list:
            key = item['vd_dealerCode']
            value = item
            dlr_dict[key] = value
        return dlr_dict

    def prase_data(self):
        dlr_list = []
        data = self.get_data()
        for v in data.values():
            dlr_list.append(v)
        return dlr_list


class GwmSpider(DykmcSpider):

    def prase_request(self):
            r = requests.get(self.js_url)  # 是get方法！
            dlr_dict = {}
            # print(r.content)
            s = bytes.decode(r.content)[55:-3]
            # print(s)
            for item in s.split('},{'):
                if len(item) > 2:
                    item.strip('{' + '[' + ']')
                    dlr = {}
                    # print(item)
                    for i in item[:-2].split('\",'):
                        # print(i)  # 此处改编码
                        try:
                            # print(i)
                            k, v = i.split(':\"')   # ID:"817" ,v是unicode
                            # print(k, v.encode('utf-8').decode('unicode_escape'))
                            dlr[k] = v.encode('utf-8').decode('unicode_escape')   # 将'\u'开头的str 转为unicode
                            # print(dlr)
                        except:
                            print(i)    # BusinessHours:"8:30-18:00"
                    key = dlr['ID']
                    value = dlr
                    dlr_dict[key] = value
                    return dlr_dict

    def prase_data(self):
        dlr_list = []
        data = self.get_data()
        for v in data.values():
            dlr_list.append(v)
        return dlr_list


class DsSpider(DykmcSpider):

    def prase_request(self):
        r = requests.get(self.js_url)  # 是get方法！
        dlr_dict = {}
        # print(r.content)
        s = bytes.decode(r.content)
        data = json.loads(s)
        dlr_list = (data['dealers'])
        for item in dlr_list:
            key = item['id']
            value = item
            dlr_dict[key] = value
        return dlr_dict

    def prase_data(self):
        dlr_list = []
        data = self.get_data()
        for v in data.values():
            dlr_list.append(v)
        return dlr_list


class BuickSpider(DykmcSpider):

    def prase_request(self):
        r = requests.get(self.js_url)  # post??
        # print(r.content)
        dlr_list = json.loads(bytes.decode(r.content))  # bytes to string, string to dict
        # print(dlr_list[1])
        dlr_dict = {}
        # s = bytes.decode(r.content)[16:]
        # dlr_list = json.loads(s)
        for item in dlr_list:
            key = item['dealerCode']
            value = item
            dlr_dict[key] = value
        return dlr_dict

    def prase_data(self):
        dlr_list = []
        data = self.get_data()
        data['SJ1220']['address'] = data['SJ1220']['address'].replace(u'\xa0', u'')
        data['SJ1535']['address'] = data['SJ1535']['address'].replace(u'\xa0', u'')
        for v in data.values():
            dlr_list.append(v)
        return dlr_list


class SvmSpider(DykmcSpider):

    def prase_request(self):
        if (self.domain + '.xml') not in os.listdir(os.getcwd()):
            r = requests.get(self.js_url)
            with open('svm.xml', 'wb') as f:
                f.write(r.content)
        else:
            tree = ET.parse('svm.xml')
            dlr_dict = {}
            root = tree.getroot()
            # print(root.tag)
            for area in root:
                for province in area:
                    for city in province:
                        for district in city:
                            for dlr in district:
                                # print(dlr.tag, dlr.attrib)
                                # print(type(dlr.attrib))
                                key = dlr.attrib['code']
                                value = dlr.attrib
                                dlr_dict[key] = value
            return dlr_dict

            # DOMTree = xml.dom.minidom.parse("svm.xml")
            # collection = DOMTree.documentElement
            # for area in collection.getElementsByTagName("area"):
            #     for province in area
            #
            # print(collection.getElementsByTagName("area")[1].getAttribute("name"))

        # print(r.content)
        # soup = BeautifulSoup(r.content, 'xml')

    def prase_data(self):
        dlr_list = []
        data = self.get_data()
        for v in data.values():
            dlr_list.append(v)
        return dlr_list


class NissanSpider(DykmcSpider):

    def prase_request(self):
        '''https://www.dongfeng-nissan.com.cn/Ajax/AjaxSupport.ashx?method=ProvinceFilter
        https://www.dongfeng-nissan.com.cn/Ajax/AjaxSupport.ashx?method=CityFilter&
        ProvinceID=4bbb4d40-fb29-4004-8938-ecc4d028caa4
        https://www.dongfeng-nissan.com.cn/Ajax/AjaxSupport.ashx?method=LoadDealerData&brand=1&
        selpro=4bbb4d40-fb29-4004-8938-ecc4d028caa4&
        selcity=c97ab985-5a52-4483-af1d-ec5df3bbe752&
        selseries='''

        dlr_dict = {}
        r_pro = requests.get(self.js_url+'?method=ProvinceFilter')   # 获取省份代码
        # print(r_pro.content)
        for province in json.loads(bytes.decode(r_pro.content)):
            # r_city = requests.get(self.js_url+'?method=CityFilter&ProvinceID='+'4bbb4d40-fb29-4004-8938-ecc4d028caa4')
            # print(r_city.content)
            r_city = requests.get(self.js_url+'?method=CityFilter&ProvinceID='+province['ItemID'])
            # print(r_city.content)
            for city in json.loads(bytes.decode(r_city.content)):
                r_dlr = requests.get(self.js_url+'?method=LoadDealerData&brand=1&selpro='\
                                     +province['ItemID']+'&selcity='\
                                     +city['ItemID'])
                # print(r_dlr.content)
                dlr_dict_ori = json.loads(bytes.decode(r_dlr.content))
                for dlr_k in dlr_dict_ori:
                    # print(dlr_k)
                    dlr_dict_ori[dlr_k]['province'] = province['Name']
                    dlr_dict_ori[dlr_k]['city'] = city['Name']
                for k, v in dlr_dict_ori.items():
                    dlr_dict[k] = v
        return dlr_dict

        # r_dlr = requests.get(self.js_url+'?method=LoadDealerData&brand=1&selpro='\
        #                      +'4bbb4d40-fb29-4004-8938-ecc4d028caa4'+'&selcity='\
        #                      +'c97ab985-5a52-4483-af1d-ec5df3bbe752')


class GhacSpider(DykmcSpider):

    def prase_request(self):
        r = requests.get(self.js_url)
        # for i in r.content.split(b';\r\n'):
        #     print(i+b'\n')
        province, city, dlr, car, _ = r.content.split(b';')
        # print(province+b'\n')
        # print(city+b'\n')
        # print(dlr+b'\n')
        province_dict = {}
        city_dict = {}
        dlr_dict = {}
        for province in json.loads(bytes.decode(province[114:])):
            key = province['PROVINCE_ID']
            value = province
            province_dict[key] = value
        for city in json.loads(bytes.decode(city[24:])):
            key = city['CITY_ID']
            value = city
            city_dict[key] = value
            city_dict['b8700d48-95f3-4455-833b-5a0c5a2f507c'] = \
                {'CITY_ID': 'b8700d48-95f3-4455-833b-5a0c5a2f507c', 'CITY_NAME':'永州',\
                 'PROVINCE_ID':"db3ab30d-4034-4426-8912-9ff648234405"}# 添加'CITY_ID': 'b8700d48-95f3-4455-833b-5a0c5a2f507c'信息，湖南省永州市
        for dlr in json.loads(bytes.decode(dlr[27:])):
            try:
                dlr['city'] = city_dict[dlr['CITY_ID']]['CITY_NAME']
                dlr['province'] = province_dict[city_dict[dlr['CITY_ID']]['PROVINCE_ID']]['PROVINCE_NAME']
            except:
                print(dlr['CITY_ID'],dlr)
            # print(dlr)
            key = dlr['CITY_ID']
            value = dlr
            dlr_dict[key] = value
        return dlr_dict


class FtmsSpider(DykmcSpider):

    def prase_request(self):
        dlr_dict = {}
        r = requests.get(self.js_url+'/province')
        # print(r.content)
        province_list = json.loads(bytes.decode(r.content))
        for province in province_list:
            # print(province)
            r= requests.get(self.js_url+'/city_stro?province='+province['name'])
            # print(r.content)
            for city in json.loads(bytes.decode(r.content)):
                for dlr in city['dealer']:
                    key = dlr['id']
                    value = dlr
                    dlr_dict[key] = value
        return dlr_dict


class DfcitroenSpider(DykmcSpider):

    def prase_request(self):
        dlr_dict = {}
        r = requests.get(self.js_url+'/dsearch')
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
            r = requests.get(self.js_url+'/api/getCities/'+k)  # http://www.dongfeng-citroen.com.cn/4s/index.php/api/getCities/3
            # print(r.content)
            for city in json.loads(bytes.decode(r.content)):
                key = city['id']
                value = city
                city_dict[key] = value
        # print(city_dict)
        for k in city_dict.keys():
            r = requests.post(self.js_url+'/api/getDealersByLocation?', data={'city':k})  # http://www.dongfeng-citroen.com.cn/4s/index.php/api/getDealersByLocation?
            # print(r.content)
            for dlr in json.loads(bytes.decode(r.content))['list']:
                dlr['city'] = city_dict[dlr['city']]['city']
                dlr['province'] = province_dict[dlr['province']]['name']
                key = dlr['id']
                value = dlr
                dlr_dict[key] = value
        return dlr_dict


class ChevroletSpider(DykmcSpider):

    def prase_request(self):
        dlr_dict = {}
        r = requests.get(self.js_url)
        dlr_list = json.loads(bytes.decode(r.content))
        for dlr in dlr_list:
            key = dlr['code']
            value = dlr
            dlr_dict[key] = value
        return dlr_dict


# class SvmSpider(DykmcSpider):
#
#     def prase_request(self):
#         pass

#     def prase_data(self):
#         pass

if __name__ == '__main__':
    dyk_url = 'http://www.dyk.com.cn/public/dyk/js/allDealersData.js'
    dyk = DykmcSpider('dyk', dyk_url)
    # print(dyk.js_url)
    # print(dyk.get_data())
    # print(dyk.prase_data())
    # dyk.export_data()

    hyundai_url = 'https://www.beijing-hyundai.com.cn/datacenter/static/js/District.js'
    hyundai = HyundaiSpider('hyundai', hyundai_url)
    # print(hyundai.js_url)
    # print(hyundai.domain)
    # hyundai.get_data()
    # hyundai.export_data()

    fawvw_url = 'http://contact.faw-vw.com/uploadfiles/js/dealer.js'   # 一汽大众
    fawvw = FawvmSpider('fawvm', fawvw_url)
    # print(fawvw.js_url)
    # print(fawvw.domain)
    # fawvw.get_data()
    # fawvw.export_data()
# print(fawvw.domain+'.json' not in os.listdir(os.getcwd()))

    gwm_url = 'http://www.gwm.com.cn/statics/gwm-cn/js/map/dealersShop.js'    # 长城
    gwm = GwmSpider('gwm', gwm_url)
    # print(gwm.js_url)
    # print(gwm.domain)
    # gwm.get_data()
    # gwm.export_data()

    ds_url = 'http://www.ds.com.cn/web/cn/api/dealers?lang=cn&type=3'    # DS
    ds = DsSpider('ds', ds_url)
    # print(ds.js_url)
    # print(ds.domain)
    # ds.get_data()
    # ds.export_data()

    buick_url = 'http://www.buick.com.cn/api/dealer.aspx'     # 别克
    buick = BuickSpider('buick', buick_url)
    # print(buick.js_url)
    # print(buick.domain)
    # buick.get_data()
    # buick.export_data()

    svm_url = 'http://club.svw-volkswagen.com/map/latlng.xml'  # 上汽大众
    svm = SvmSpider('svm', svm_url)
    # print(svm.js_url)
    # print(svm.domain)
    # svm.get_data()
    # svm.export_data()

    nissan_url = 'https://www.dongfeng-nissan.com.cn/Ajax/AjaxSupport.ashx'   #  东风日产
    nissan = NissanSpider('nissan', nissan_url)
    # print(nissan.js_url)
    # print(nissan.domain)
    # nissan.get_data()
    # nissan.export_data()

    ghac_url = 'http://www.ghac.cn/js/Official/staticData/p_c_dealers_data.js'  # 广汽本田
    ghac = GhacSpider('ghac', ghac_url)
    # print(ghac.js_url)
    # print(ghac.domain)
    # ghac.get_data()
    # ghac.export_data()

    ftms_url = 'http://www.ftms.com.cn/app/dealer'  # 一汽丰田
    ftms = FtmsSpider('ftms', ftms_url)
    # print(ftms.js_url)
    # print(ftms.domain)
    # ftms.get_data()
    # ftms.export_data()

    dfcitroen_url = 'http://www.dongfeng-citroen.com.cn/4s/index.php'  # 东风雪铁龙
    dfcitroen = DfcitroenSpider('dfcitroen', dfcitroen_url)
    # print(dfcitroen.js_url)
    # print(dfcitroen.domain)
    # dfcitroen.get_data()
    # dfcitroen.export_data()
    #
    chevrolet_url = 'http://www.mychevy.com.cn/images/files/indexmap.txt'  # 雪佛兰
    chevrolet = ChevroletSpider('chevrolet', chevrolet_url)
    print(chevrolet.js_url)
    print(chevrolet.domain)
    chevrolet.get_data()
    chevrolet.export_data()

    # buick_url = 'http://www.buick.com.cn/api/dealer.aspx'  # 东风标致
    # buick = BuickSpider('buick', buick_url)
    # print(buick.js_url)
    # print(buick.domain)
    # buick.get_data()
    # buick.export_data()
    #
    # buick_url = 'http://www.buick.com.cn/api/dealer.aspx'  # 广汽丰田
    # buick = BuickSpider('buick', buick_url)
    # print(buick.js_url)
    # print(buick.domain)
    # buick.get_data()
    # buick.export_data()
    #
    # buick_url = 'http://www.buick.com.cn/api/dealer.aspx'  # 吉利汽车
    # buick = BuickSpider('buick', buick_url)
    # print(buick.js_url)
    # print(buick.domain)
    # buick.get_data()
    # buick.export_data()
    #
    # buick_url = 'http://www.buick.com.cn/api/dealer.aspx'  # 斯柯达
    # buick = BuickSpider('buick', buick_url)
    # print(buick.js_url)
    # print(buick.domain)
    # buick.get_data()
    # buick.export_data()
    #
    # buick_url = 'http://www.buick.com.cn/api/dealer.aspx'  # 长安福特
    # buick = BuickSpider('buick', buick_url)
    # print(buick.js_url)
    # print(buick.domain)
    # buick.get_data()
    # buick.export_data()
    #
    # buick_url = 'http://www.buick.com.cn/api/dealer.aspx'  # 长安汽车
    # buick = BuickSpider('buick', buick_url)
    # print(buick.js_url)
    # print(buick.domain)
    # buick.get_data()
    # buick.export_data()
    #
    # buick_url = 'http://www.buick.com.cn/api/dealer.aspx'  # 上汽通用
    # buick = BuickSpider('buick', buick_url)
    # print(buick.js_url)
    # print(buick.domain)
    # buick.get_data()
    # buick.export_data()
    #
    # buick_url = 'http://www.buick.com.cn/api/dealer.aspx'  # 神龙汽车
    # buick = BuickSpider('buick', buick_url)
    # print(buick.js_url)
    # print(buick.domain)
    # buick.get_data()
    # buick.export_data()
    #
    # buick_url = 'http://www.buick.com.cn/api/dealer.aspx'  # 比亚迪
    # buick = BuickSpider('buick', buick_url)
    # print(buick.js_url)
    # print(buick.domain)
    # buick.get_data()
    # buick.export_data()
    #
    # buick_url = 'http://www.buick.com.cn/api/dealer.aspx'  # 东风本田
    # buick = BuickSpider('buick', buick_url)
    # print(buick.js_url)
    # print(buick.domain)
    # buick.get_data()
    # buick.export_data()
    #
    # buick_url = 'http://www.buick.com.cn/api/dealer.aspx'  # 其他
    # buick = BuickSpider('buick', buick_url)
    # print(buick.js_url)
    # print(buick.domain)
    # buick.get_data()
    # buick.export_data()