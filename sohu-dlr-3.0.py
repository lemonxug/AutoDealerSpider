import requests
from lxml import etree
import json
import csv
import time
import random
import _thread

def get_province_info(url):

    r = requests.get(url)
    province_dict = {}
    provincelist = json.loads(bytes.decode(r.content).split('= ')[1])
    for i in provincelist:
        # print(i)
        province_dict[i['id']] = i['name'][2:]
    return  province_dict


def get_city_info(url):

    r = requests.get(cityarr)
    city_dict = {}
    citydict = json.loads(bytes.decode(r.content).split('= ')[1])
    for k, v in citydict.items():
        for c in v:
            # print(k,c.values())
            city_dict[c['id']] = {'id':c['id'], 'city':c['name'][2:],
                                  'province':province_dict[k]}
    return city_dict


def get_dlrinfo_html(citycode, brandid, proxies=None):

    query_url = 'http://dealer.auto.sohu.com/map/?city='+str(citycode)+'&brandId='+str(brandid)
    post_data = {
        'lastSelect': [],
        'userSelect': ["b"+str(brandid)],
        'lastMode': 1
    }
    response = requests.post(query_url, data=post_data, headers=headers, proxies=proxies)
    return response


def prase_dlr_info(response, brandid):

    html = etree.HTML(bytes.decode(response.content))
    data = html.xpath('//script[2]/text()')
    dealer_list = []
    dlrlist = json.loads(data[0].split('\n')[1][22:-2])
    for dlr in dlrlist:
        # print(dlr)
        dealer = {
            'brand': brand_dict[brandid],
            'name' : dlr['zhName'],
            'city':city_dict[citycode]['city'],
            'province':city_dict[citycode]['province'],
            'address':dlr['address'],
            'coordinate':dlr['coordinate'],
        }
        print(dealer)
        dealer_list.append(dealer)

    return dealer_list


def get_brand_list(citycode):

    params1 = {
    'cityCode' : citycode
    }
    r = requests.get(abc_url, params=params1)
    abc_list = json.loads(bytes.decode(r.content))
    brand_list =[]
    for character in abc_list:
        params2 = {
        'cityCode' : citycode ,
        'alphabet' : character
        }
        r = requests.get(brand_url, params=params2)
        tmp = json.loads(bytes.decode(r.content))
        # print(tmp)
        brand_list.extend(tmp)
    # print(brand_list)
    return brand_list


def get_proxy(url):
    r = requests.get(url)
    # print(r.text)
    n = random.randint(0, 100)
    line = r.text.split('\n')[n]
    ip, port = line.split(':')
    proxies = {
        'http': 'http://%s:%s' % (ip, port),
        'https': 'http://%s:%s' % (ip, port)
    }
    print(proxies)
    return proxies
    # ip_ports = json.loads(r.text)

if __name__ == "__main__":

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
        'Referer': 'http://dealer.auto.sohu.com/map/?city=320100'
    }
    provincearr = 'http://auto.sohu.com/dealer/static/provinceArr.js'
    cityarr = 'http://auto.sohu.com/dealer/static/cityArr.js'
    brand_url = 'http://dealer.auto.sohu.com/map/ajaxGetOnSellBrandListByCityAndAlphabet'
    abc_url = 'http://dealer.auto.sohu.com/map/ajaxGetOnSellBrandAlphabetListByCity'
    # query_url = 'http://dealer.auto.sohu.com/map/?city=320100&brandId=191'
    proxy_url = 'http://7xrnwq.com1.z0.glb.clouddn.com/proxy_list.txt?v=2000'
    # proxies = get_proxy(proxy_url)
    # get_proxy(proxy_url)
    province_dict = get_province_info(provincearr)
    # print(province_dict)
    city_dict = get_city_info(cityarr)
    # print(city_dict)
    brand_dict  = {}
    dealer_list = []
    count = 1
    for citycode in city_dict.keys():
        brand_list = get_brand_list(citycode)
        # print(citycode, brand_list)
        try:
            for brand in brand_list: #  brand['id'], brand['name']
                brand_dict[brand['id']]=brand['name']
                # try:
                    # with open('log-all', 'a') as f:
                    #     f.write(citycode+","+ city_dict[citycode]+','+brand['id']+','+brand['name']+'\n')
                r = get_dlrinfo_html(citycode, brand['id'],)
                tmp = prase_dlr_info(r, brand['id'])
                # for d in tmp:
                #     f.write(str(d)+'\n')
                dealer_list.extend(tmp)
                count += 1
                if  count % 10 == 0:
                    print(len(dealer_list))
                    time.sleep(10)
        except:
            with open('log', 'a') as f:
                f.write(citycode+','+str(brand_list)+'\n')

    #  试试多线程，队列，明天去学习吧！！
    #     for brand in brand_list:
    #         brand_dict[brand['id']] = brand['name']
    #         r = _thread.start_new_thread(get_dlrinfo_html, args=(citycode, brand['id'],proxies))
    with open('sohu.csv', 'w', encoding='gbk', newline='') as f:
        w = csv.writer(f)
        for d in dealer_list:
            w.writerow(d.values())
