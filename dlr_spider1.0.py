# -*- coding : utf-8 -*-

import json
import csv
import requests
import os
from bs4 import BeautifulSoup
import re
import xml.etree.ElementTree as ET   # 解析XML文件
import xml.dom.minidom   # 解析XML文件
from urllib import parse


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


class PeugeotSpider(DykmcSpider):

    def prase_request(self):
        pass

    def prase_data(self):
        pass


class GactoyotaSpider(DykmcSpider):

    def prase_request(self):
        dlr_dict={}
        province_dict={}
        city_dict={}
        r = requests.get(self.js_url+'/buy/shopping/dealer-search')
        soup = BeautifulSoup(r.content, 'lxml')
        # print(soup.find(id="ddlProvince").contents)
        for option in soup.find(id="ddlProvince").contents:
            if option.string !=  '\n':

            #     print(option['value'])
                province = {}
                key = option['value']
                value = option.string
                province['value'] = key
                province['name'] = value
                province_dict[key] = province
        for key in province_dict.keys():
            r = requests.get(self.js_url+\
                             '/Ajax/CommonHandler.ashx?method=City&ProvinceID='+key)
            for city in json.loads(bytes.decode(r.content)):
                key = city['Code']
                value = city
                city_dict[key] = value
        for key in city_dict.keys():
            r = requests.get(self.js_url+\
                             '/Ajax/DealerHandler.ashx?method=GetDealerDetailByCity&cityId='\
                             +key+'&keyWord=&dealerCode=')
            for dlr in json.loads(bytes.decode(r.content)):
                key = dlr['DealerCode']
                dlr_dict[key] = dlr
        return dlr_dict


class GeelySpider(DykmcSpider):

    def prase_request(self):
        carxid_dict = {}
        province_dict = {}
        city_dict = {}
        dlr_dict = {}
        r = requests.get(self.js_url+'/network')
        soup = BeautifulSoup(r.content, 'lxml')
        for option in soup.find(id='sel_region'):
            if option.string != '\n':
                # print(option.string)
                province = {}
                key = option['value']
                value = option.string
                province['value'] = key
                province['name'] = value
                province_dict[key] = province
        for key in province_dict.keys():
            r = requests.get('http://mall.geely.com/index.php/dealer/change_resion/'+key)
            soup =  BeautifulSoup(r.content, 'lxml')
            for op in soup.find_all('option'):
                key = op['value']
                value = op.string
                # print(key,value)
                city = {}
                city['code'] = key
                city['name'] = value
                city_dict[key] = city
        for key in city_dict.keys():
            r = requests.get('http://mall.geely.com/index.php/dealer/dealer_resion_map?cid='+key+'&carx=0&kw=')
            for dlr in json.loads(bytes.decode(r.content))['data']:
                key = dlr['id']
                dlr_dict[key] = dlr
        return dlr_dict


class SkodaSpider(DykmcSpider):

    def prase_request(self):
        dlr_dict = {}
        r = requests.get(self.js_url)
        data = bytes.decode(r.content)
        p1 = re.compile('window.DEALERS_DATA.\w* = ')
        m1 = p1.split(data)
        # nrssc : 分销中心\r\nprovince : 省份\r\ncity : 城市\r\ndistrict : 区县\r\ndealer : 经销商
        nrssc = json.loads(m1[1].strip()[:-1])
        province = json.loads(m1[2].strip()[:-1])
        city = json.loads(m1[3].strip()[:-1])
        district = json.loads(m1[4].strip()[:-1])
        dealer = json.loads(m1[5].strip()[:-1])
        # xy = json.loads(m1[6].strip()[:-1])
        # print(dealer['columnCount'])
        # print(dealer['columnNames'])
        columns = ['code', 'name', 'rssc_code', 'province_code', 'city_code',
        'district_code', 'phone', 'fax', 'email', 'address', 'service_tel', 'hot_line']
        for item in dealer['data']:
            dlr = {}
            for x, y in zip(columns, item):
                dlr[x] = y
            print(dlr)
            key = item[0]
            dlr_dict[key] = dlr
        return dlr_dict


class FordSpider(DykmcSpider):   # 待定 doing-1

    def prase_request(self):
        province_dict = {}
        dlr_dict = {}
        url = 'https://www.ford.com.cn/content/ford/cn/zh_cn/configuration/application-and-services-config/provinceCityDropDowns.multiFieldDropdown.data'
        r = requests.get(url)
        # print(r.content)
        province_list = json.loads(bytes.decode(r.content))
        for p  in province_list:
            # print(p['provinceKey'])
            for c in p['cityList']:
                # file_url = parse.quote(data['Entity'][5:])
                # 获取中心经纬度
                url = 'https://restapi.amap.com/v3/geocode/geo?key=1891d0f847c0a210a88015fdd4c3bc46&s=rsv3&callback=jsonp_232&platform=JS&logversion=2.0&sdkversion=1.3&appname=http://www.ford.com.cn/dealer/locator?intcmp=hp-return-fd&csid=D6C889F7-2FF1-4EA5-8D60-494D42872518&'+\
                      'address='+ parse.quote(p['provinceKey'])+\
                      parse.quote(c['cityKey'])\
                      # +'&callback=jsonp_232&_=1510383274081'
                r = requests.get(url)
                # print(r.content)
                tmp = json.loads(bytes.decode(r.content)[10:-1])
                # print(tmp)
                # print(tmp['geocodes'][0]['location'])
                url = 'https://yuntuapi.amap.com/datasearch/around?s=rsv3&key=1891d0f847c0a210a88015fdd4c3bc46&extensions=base&language=en&enc=utf-8&output=jsonp&sortrule=_distance:1&keywords=&limit=100&tableid=55adb0c7e4b0a76fce4c8dd6&radius=35000&callback=jsonp_333&platform=JS&logversion=2.0&sdkversion=1.3&appname=http://www.ford.com.cn/dealer/locator?intcmp=hp-return-fd&csid=C0F2C0C7-D2A2-4730-9618-5B2C060C3DDD&'+\
                      'center='+tmp['geocodes'][0]['location']+\
                      '&filter=AdministrativeArea:'\
                      +parse.quote(p['provinceKey'])\
                      +' Locality:'\
                      +parse.quote(c['cityKey'])
                      # +'&callback=jsonp_333&_='\
                      # +'1510383274082'
                # print(url)
                # # url = parse.quote(url)
                try:
                    r = requests.get(url)
                # print(r.content)
                    tmp = json.loads(bytes.decode(r.content)[10:-1])
                    for d in tmp['data']:
                        dlr = {}
                        key = d['_id']
                        dlr[key] = d
                        dlr_dict[key] = dlr
                except:
                    pass
        return dlr_dict
    def prase_data(self):
        pass


class ChanganSpider(DykmcSpider):   # 待定

    def prase_request(self):
        pass

    def prase_data(self):
        pass


class BydSpider(DykmcSpider):

    def prase_request(self):
        dlr_dict = {}
        r = requests.get(self.js_url)
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
            r = requests.post('http://www.bydauto.com.cn/ajax.php?act=getpro&inajax=1',data=postdata)
            soup = BeautifulSoup(r.content, 'lxml')
            for op1 in soup.find_all('option'):
                postdata = {'pid': op1.string, 'carid' : k}
                r = requests.post('http://www.bydauto.com.cn/ajax.php?act=getcity&inajax=1', data = postdata)
                soup = BeautifulSoup(r.content, 'lxml')
                try:
                    for op2 in soup.find_all('option'):
                        postdata = {'showtype':'json','cid':op2.string,'carid':k}
                        r = requests.post('http://www.bydauto.com.cn/ajax.php?act=getsellpoint&inajax=1', data=postdata)
                        for dlr in json.loads(bytes.decode(r.content)):
                            key = dlr['id']
                            dlr_dict[key] = dlr
                except:
                    print(k, op1.string)
        return dlr_dict
        # print(car_dict)

    def prase_data(self):
        dlr_list = []
        data = self.get_data()
        data['1775']['phone'] = data['1775']['phone'].replace('\xa0', '')
        data['1966']['address'] = data['1966']['address'].replace('\xa0', '')
        data['1929']['address'] = data['1929']['address'].replace('\xa0', '')
        for dlr in data.values():
            dlr_list.append(dlr)
        return dlr_list


class HondaSpider(DykmcSpider):   # 官网没有数据

    def prase_request(self):
        pass

    def prase_data(self):
        pass


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
    # print(chevrolet.js_url)
    # print(chevrolet.domain)
    # chevrolet.get_data()
    # chevrolet.export_data()

    # 跳过
    peugeot_url = 'http://www.peugeot.com.cn/api/dealer.aspx'  # 东风标致 - 跳过
    peugeot = PeugeotSpider('peugeot', peugeot_url)
    # print(peugeot.js_url)
    # print(peugeot.domain)
    # peugeot.get_data()
    # peugeot.export_data()

    gactoyota_url = 'https://www.gac-toyota.com.cn'  # 广汽丰田
    gactoyota = GactoyotaSpider('gactoyota', gactoyota_url)
    # print(gactoyota.js_url)
    # print(gactoyota.domain)
    # gactoyota.get_data()
    # gactoyota.export_data()

    geely_url = 'http://mall.geely.com/index.php'  # 吉利汽车
    geely = GeelySpider('geely', geely_url)
    # print(geely.js_url)
    # print(geely.domain)
    # geely.get_data()
    # geely.export_data()

    skoda_url = 'http://www.skoda.com.cn/assets/js/apps/dealerdata.js'  # 斯柯达
    skoda = SkodaSpider('skoda', skoda_url)
    # print(skoda.js_url)
    # print(skoda.domain)
    # skoda.get_data()
    # skoda.export_data()

    ford_url = 'http://www.ford.com.cn/api/dealer.aspx'  # 长安福特  - 跳过  -doing
    ford = FordSpider('ford', ford_url)
    print(ford.js_url)
    print(ford.domain)
    ford.get_data()
    # ford.export_data()

    changan_url = 'http://www.changan.com.cn/api/dealer.aspx'  # 长安汽车
    changan = ChanganSpider('changan', changan_url)
    # print(changan.js_url)
    # print(changan.domain)
    # changan.get_data()
    # changan.export_data()

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
    byd_url = 'http://www.bydauto.com.cn/counter-sellpoint.html'  # 比亚迪
    byd = BydSpider('byd', byd_url)
    # print(byd.js_url)
    # print(byd.domain)
    # byd.get_data()
    # byd.export_data()
    #
    honda_url = 'http://www.honda.com.cn/api/dealer.aspx'   # 东风本田  # 跳过，页面是静态的，没有经销商信息
    honda = HondaSpider('honda', honda_url)
    # print(honda.js_url)
    # print(honda.domain)
    # honda.get_data()
    # honda.export_data()
    #
    # buick_url = 'http://www.buick.com.cn/api/dealer.aspx'  # 其他
    # buick = BuickSpider('buick', buick_url)
    # print(buick.js_url)
    # print(buick.domain)
    # buick.get_data()
    # buick.export_data()