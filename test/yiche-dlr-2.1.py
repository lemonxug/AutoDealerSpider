import requests
from lxml import etree
import json
import csv
import time
import re
from random import choice
import threading
dealer_list = []
lock = threading.Lock()
delay = 1
count = 0

def get_proxy():

    r = requests.get('http://127.0.0.1:8000/?protocol=0&count=100&country=国内')
    ip_ports = json.loads(r.text)
    # print(ip_ports}
    # ip = ip_ports[0][0]
    # port = ip_ports[0][1]
    proxies = []
    for ip_port in ip_ports:
        ip = ip_port[0]
        port = ip_port[1]
        proxy = {
            'http': 'http://%s:%s' % (ip, port),
            # 'https': 'http://%s:%s' % (ip, port)
        }
        proxies.append(proxy)
    # print(proxies)
        return proxies
proxies = get_proxy()

USER_AGENT_LIST = [
    'Mozilla/4.0 (compatible; MSIE 5.0; SunOS 5.10 sun4u; X11)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser;',
    'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1)',
    'Microsoft Internet Explorer/4.0b1 (Windows 95)',
    'Opera/8.00 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 5.0; AOL 4.0; Windows 95; c_athome)',
    'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; ZoomSpider.net bot; .NET CLR 1.1.4322)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; QihooBot 1.0 qihoobot@qihoo.net)',
]
def get_headers():
    headers = []
    for ua in USER_AGENT_LIST:
        header = {
            'User-Agent': ua,
            'Referer': 'http://dealer.bitauto.com/beijing/audi/'
        }
        headers.append(header)
    return headers
headers = get_headers()

def get_province_info():
    url = 'http://auto.sohu.com/dealer/static/provinceArr.js'
    r = requests.get(url)
    province_dict = {}
    provincelist = json.loads(bytes.decode(r.content).split('= ')[1])
    for i in provincelist:
        # print(i)
        province_dict[i['id'][:2]] = i['name'][2:]
    return  province_dict
provincedict = get_province_info()

def get_citylist():
    url = 'http://api.admin.bitauto.com/city/getcity.ashx?'
    params = {
        'callback':'City_Select._$JSON_callback.$JSON',
        'requesttype':'json',
        'bizCity':1
    }
    r = requests.get(url,params=params, headers=choice(headers))
    citylist = json.loads(bytes.decode(r.content[34:-2]))

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
    r = requests.get(url, params=params, headers=choice(headers),proxies=choice(proxies))
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
    brandlist = []
    for i, na, u, nu in zip(id,name,url,num):
        brand = {
            'id' : i,
            'name': na,
            'url': u,
            'num': nu,
            'regionid':city['regionId'],
            'city':city['regionName'],
            'province': provincedict[city['parentId'][:2]]
        }
        brandlist.append(brand)
        # time.sleep(10)
    c = 0
    # print(len(brandlist))
    for brand in brandlist:
        c += 1
        if c % 3 == 0:
            print(count)
            time.sleep(2)
        # print(brand)
        get_district(brand)

    # print(len(brandlist))
    # return brandlist


url = 'http://dealer.bitauto.com'
def get_district(brand):

    global delay
    delay += 1
    suburl = brand['url']
    r = requests.get(url+suburl, headers=choice(headers), proxies=choice(proxies))
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
        # time.sleep(10)
    if len(districtlist) != 0:

        # print(districtlist)
        for district in districtlist:
            lock.acquire()
            try:
                get_dlrinfo(district)
                # time.sleep(2)
            except:
                print('')
            finally:
                lock.release()
    # print(districtlist)
    # return districtlist


def get_dlrinfo(district):
    suburl = district['href']
    r = requests.get(url+suburl, headers=choice(headers),proxies=choice(proxies))

    html = etree.HTML(bytes.decode(r.content))
    for dlr in  html.xpath('//div[@class="row dealer-list"]'):
        dealer = {
            'category':dlr.xpath('.//h6/a/em/text()')[0],
            'name': dlr.xpath('.//h6/a/text()')[0],
            'brand': district['brand'],
            'id':dlr.xpath('.//p[@class="tel"]/span[2]/@id')[0],
            'address':dlr.xpath('.//p[@class="add"]/span/@title')[1],
            'district':district['name'],
            'city': district['city'],
            'province':district['province'],
            'brand-info':dlr.xpath('.//p[@class="brand"]/text()')[0],
        }
        global count
        count += 1
        # print(dealer)
        dealer_list.append(dealer)

        with open('yiche-3.csv', 'a', newline='') as f:
            w = csv.writer(f)
            try:
                print(dealer)
                w.writerow(dealer.values())
            except:
                print("failed crawl ", dealer)
        # time.sleep(2)

tmp = {'category': '4S店', 'name': '北京奥迪金港店', 'brand': '奥迪', 'id': '100040078', 'address': '北京市朝阳区金盏乡东苇路北京金港汽车公园...', 'district': '朝阳区', 'city': '北京市', 'province': '北京', 'brand-info': '进口Audi Sport,进口奥迪,一汽-大众奥迪'}

# provincedict = {'340000': '安徽省', '110000': '北京', '500000': '重庆', '350000': '福建省', '440000': '广东省',
#                 '450000': '广西壮族自治区', '520000': '贵州省', '620000': '甘肃省', '130000': '河北省', '230000': '黑龙江省',
#                 '410000': '河南省', '420000': '湖北省', '430000': '湖南省', '460000': '海南省', '220000': '吉林省',
#                 '320000': '江苏省', '360000': '江西省', '210000': '辽宁省', '150000': '内蒙古自治区', '640000': '宁夏回族自治区',
#                 '630000': '青海省', '140000': '山西省', '310000': '上海', '370000': '山东省', '510000': '四川省',
#                 '610000': '陕西省', '120000': '天津', '990000': '990000', '540000': '西藏自治区', '650000': '新疆维吾尔自治区',
#                 '530000': '云南省', '330000': '浙江省','419000': '河南省','429000':'湖南省','469000': '海南省'}

def main():
    # print(len(provincedict))
    # with open('yiche-3.csv', 'a', newline='') as f :
    #     w = csv.writer(f)
    #     w.writerow(tmp.keys())
    threads = []
    # print(get_citylist())
    c = 0
    for city in get_citylist():
        c += 1
        print(city)
        t = threading.Thread(target=get_brandlist,args=(city, ))
        if c % 10 == 0:
            # time.sleep(1)
            print(count)
        t.start()
        threads.append(t)
        for t in threads:
            t.join()
            # print(len(get_brandlist(city)))
            # for brand in get_brandlist(city):
            #     print(len(get_district(brand)))
        #         for district in get_district(brand):
        #             t = threading.Thread(target=get_dlrinfo,args=(district, w))
        #             t.start()
        #             threads.append(t)
        #             delay += 1
        #             print(delay)
        #             # if delay%10 == 0:
        #             #     print(count)
        #             #     time.sleep(10)
        # for t in threads:
        #     t.join()



if __name__ == '__main__':
    with open('yiche-3.csv', 'a', newline='') as f :
        w = csv.writer(f)
        w.writerow(tmp.keys())
    start = time.time()
    # city = get_citylist()[0]
    # brand = get_brandlist(city)[0]
    # district = get_district(brand)[0]
    # get_dlrinfo(district)
    main()
    end = time.time()
    print('耗时：'+str((end-start)/60)+'分钟')