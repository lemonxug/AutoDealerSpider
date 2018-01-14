import requests
from lxml import etree
import json
import csv
import time
import re


url1 = 'http://dealer.bitauto.com/beijing/audi/'
# url2= 'http://api.car.bitauto.com/CarInfo/getlefttreejson.ashx?tagtype=jingxiaoshang&pagetype=masterbrand&objid=0&citycode=suzhou%2F&cityid=1502'
url2= 'http://api.car.bitauto.com/CarInfo/getlefttreejson.ashx?'
url3 = 'http://api.admin.bitauto.com/city/getcity.ashx?\
callback=City_Select._$JSON_callback.$JSON&requesttype=json&bizCity=1'
url = 'http://dealer.bitauto.com/beijing/audi/?BizModes=0'
query_url = 'http://dealer.bitauto.com/DealerDetail/GetDealerDetail/?dealerid=100040593'

pinyin_url = 'http://image.bitautoimg.com/index/js/CitySelectModule.v2.js?v=1'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
    # 'Referer': 'http://dealer.auto.sohu.com/map/?city=320100'
}

def get_province_info():
    url = 'http://auto.sohu.com/dealer/static/provinceArr.js'
    r = requests.get(url)
    province_dict = {}
    provincelist = json.loads(bytes.decode(r.content).split('= ')[1])
    for i in provincelist:
        # print(i)
        province_dict[i['id']] = i['name'][2:]
    return  province_dict
provincedict = get_province_info()

def get_citylist():
    url = 'http://api.admin.bitauto.com/city/getcity.ashx?'
    params = {
        'callback':'City_Select._$JSON_callback.$JSON',
        'requesttype':'json',
        'bizCity':1
    }
    r = requests.get(url,params=params, headers=headers)
    # print(r.content)
    citylist = json.loads(bytes.decode(r.content[34:-2]))
    # print(citylist)
    # [{'cityId': '2823', 'regionId': '654000', 'cityName': '伊犁哈萨克自治州',
    # 'regionName': '伊犁哈萨克自治州', 'cityPinYin': 'yilihasakezizhizhou',
    # 'shortName': '伊犁', 'parentId': '650000', 'cityLevel': '3',
    # 'domain': '0', 'navCityId': '2801', 'centerCityId': '2801',
    # 'bizCity': '1', 'natureType': '2'},]
    # print(citylist)
    return citylist
# for city in citylist: # city is dict, keys: cityId, regionId, regionName, cityPinYin, parentId
    # print(city['cityId'],city['cityPinYin'])
# get_citylist()
def get_brandlist(city):
    url = 'http://api.car.bitauto.com/CarInfo/getlefttreejson.ashx?'
    params = {
        'tagtype':'jingxiaoshang',
        'pagetype':'masterbrand',
        'objid':0,
        'citycode': city['cityPinYin']+'/',  #'suzhou/',
        'cityid':city['cityId'],  #1502
    }
    r = requests.get(url, params=params,headers=headers)
    # print(bytes.decode(r.content[14:-1]))
    brandstr = bytes.decode(r.content[14:-1])
    p1 = re.compile(r'id:(\d+)')
    p2 = re.compile(r'name:"(.+?)"')
    p3 = re.compile(r'url:"(.+?)"')
    p4 = re.compile(r'num:(\d+)')
    id = re.findall(p1,brandstr)
    name = re.findall(p2,brandstr)
    url = re.findall(p3,brandstr)
    num = re.findall(p4,brandstr)
    # print(len(id),len(name),len(url),len(num))
    # for i, n, u, nu in zip(id, name, url, num):
    #     print(i,n,u,nu)
    brandlist = []
    for i, na, u, nu in zip(id,name,url,num):
        brand = {
            'id' : i,
            'name': na,
            'url': u,
            'num': nu,
            'regionid':city['regionId'],
            'city':city['regionName'],
            'province': provincedict[city['parentId']]
        }
        brandlist.append(brand)
    # print(brandlist)
    # for i in brandlist:
    #     print(i)
    return brandlist
# get_brandlist('suzhou/', 1502)

url = 'http://dealer.bitauto.com'
def get_district(brand):
    suburl = brand['url']
    # print(url+suburl)
    r = requests.get(url+suburl)
    # print(r.content)
    html = etree.HTML(bytes.decode(r.content))
    districtlist = []
    # 直辖市要区分
    if brand['regionid'] in ['110100','120100','500100','310100']:
        href = html.xpath('//dl[@id="cityarea"]//a/@href')
        district = html.xpath('//dl[@id="cityarea"]//a/text()')

    else:
        href = html.xpath('//div[@class="area-sub"]//a/@href')
        district = html.xpath('//div[@class="area-sub"]//a/text()')
    for h, d in zip(href, district):
        districtdict = {
            'href': h,
            'name':d,
            'brand':brand['name'],
            'city':brand['city'],
            'province':brand['province'],
        }
        districtlist.append(districtdict)
    # print(districtlist)
    return districtlist
    # for i in html.xpath('//div[@class="area-sub"]//a/@href'):
    #     print(i)
# get_district('/suzhou/audi/')
count = 0
def get_dlrinfo(district, writer):
    suburl = district['href']
    r = requests.get(url+suburl)
    html = etree.HTML(bytes.decode(r.content))
    for dlr in  html.xpath('//div[@class="row dealer-list"]'):
        # print(dlr.xpath('.//p[@class="add"]/span/text()'))
        dealer = {
            'category':dlr.xpath('.//h6/a/em/text()')[0],
            'name': dlr.xpath('.//h6/a/text()')[0],
            'brand': district['brand'],
            'id':dlr.xpath('.//p[@class="tel"]/span[2]/@id')[0],
            'address':dlr.xpath('.//p[@class="add"]/span/text()')[1],
            'district':district['name'],
            'city': district['city'],
            'province':district['province'],
            'brand-info':dlr.xpath('.//p[@class="brand"]/text()')[0],
        }
        global count
        count += 1
        print(dealer)
        writer.writerow(dealer.values())

tmp = {'category': '4S店', 'name': '北京奥迪金港店', 'brand': '奥迪', 'id': '100040078', 'address': '北京市朝阳区金盏乡东苇路北京金港汽车公园...', 'district': '朝阳区', 'city': '北京市', 'province': '北京', 'brand-info': '进口Audi Sport,进口奥迪,一汽-大众奥迪'}

def main():
    with open('yiche.csv', 'a', newline='') as f :
        w = csv.writer(f)
        w.writerow(tmp.keys())
        delay = 1
        for city in get_citylist():
            for brand in get_brandlist(city):
                for district in get_district(brand):
                    get_dlrinfo(district, w)
                    delay += 1
                    if delay%10 == 0:
                        print(count)
                        time.sleep(10)



if __name__ == '__main__':
    city = get_citylist()
    print(city)
    # city = get_citylist()[0]
    # brand = get_brandlist(city)[0]
    # district = get_district(brand)[0]
    # get_dlrinfo(district)
    # main()