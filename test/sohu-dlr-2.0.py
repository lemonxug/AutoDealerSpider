import requests
from lxml import etree
import json
import csv
import time
dealer_list = []

f = open('sohu.csv', 'w', encoding='gbk', newline='')
w = csv.writer(f)
w.writerow(['brand','name','city','province','address','coordinate'])

provincearr = 'http://auto.sohu.com/dealer/static/provinceArr.js'
cityarr = 'http://auto.sohu.com/dealer/static/cityArr.js'

url = 'http://dealer.auto.sohu.com/map/?city=320100&brandId=191'

r = requests.get(provincearr)
province_dict = {}
provincelist = json.loads(bytes.decode(r.content).split('= ')[1])
for i in provincelist:
    # print(i)
    province_dict[i['id']] = i['name'][2:]
# for k,v in province_dict.items():
#     print(k,v)

r = requests.get(cityarr)
city_dict = {}
citydict = json.loads(bytes.decode(r.content).split('= ')[1])
for k, v in citydict.items():
    for c in v:
        # print(k,c.values())
        city_dict[c['id']] = {'id':c['id'], 'city':c['name'][2:],
                              'province':province_dict[k]}

# for k,v in city_dict.items():
#     print(k,v)

header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
    'Referer':'http://dealer.auto.sohu.com/map/?city=320100'
}

brand_url = 'http://dealer.auto.sohu.com/map/ajaxGetOnSellBrandListByCityAndAlphabet'
abc_url = 'http://dealer.auto.sohu.com/map/ajaxGetOnSellBrandAlphabetListByCity'
query_url = 'http://dealer.auto.sohu.com/map/?city=320100&brandId=191'
def get_dlrlist(citycode, brandid, brandname):
    query_url = 'http://dealer.auto.sohu.com/map/?city='+str(citycode)+'&brandId='+str(brandid)
    post_data = {
        'lastSelect': [],
        'userSelect': ["b"+str(brandid)],
        'lastMode': 1
    }
    r = requests.post(query_url, data=post_data, headers=header)
    html = etree.HTML(bytes.decode(r.content))
    # print(html.xpath('//script[2]/text()'))
    data = html.xpath('//script[2]/text()')

    dlrlist = json.loads(data[0].split('\n')[1][22:-2])
    for dlr in dlrlist:
        # print(dlr)
        dealer = {
            'brand':brandname,
            'name' : dlr['zhName'],
            'city':city_dict[citycode]['city'],
            'province':city_dict[citycode]['province'],
            'address':dlr['address'],
            'coordinate':dlr['coordinate'],
        }
        print(dealer)
        w.writerow(dealer.values())
        # dealer_list.append(dealer)
        # time.sleep(1)

# get_dlrlist(320100, 191)

def get_brandid(citycode):
    params1 = {
    'cityCode' : citycode
    }
    r = requests.get(abc_url,params=params1)
    # print(r.content)
    abc_list = json.loads(bytes.decode(r.content))
    for c in abc_list:
        params2 = {
        'cityCode' : citycode ,
        'alphabet' : c
        }
        r = requests.get(brand_url, params=params2)
        brand_list = json.loads(bytes.decode(r.content))
        # print(brand_list)
        for brand in brand_list:
            get_dlrlist(citycode, brand['id'], brand['name'])
            time.sleep(2)

# get_brandid(340100)

for citycode in city_dict.keys():
    get_brandid(citycode)

f.close()
# with open('sohu.csv', 'w', encoding='gbk', newline='') as f:
#     w = csv.writer(f)
#     for d in dealer_list:
#         w.writerow(d.values())
