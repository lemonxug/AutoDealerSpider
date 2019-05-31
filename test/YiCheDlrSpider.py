import requests
from threading import Thread, Lock
from queue import Queue
import time
import json
from random import choice
import re
from lxml import etree
import csv


class Fetcher(object):

    def __init__(self, threads):
        self.provincedict = self.get_province_info()
        self.lock = Lock()
        self.q_city = Queue()
        self.q_brand = Queue()
        self.q_district = Queue()
        self.q_dlr = Queue()
        self.count = 0
        self.threads = threads
        self.running = 0
        self.USER_AGENT_LIST = [
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

    def __del__(self):
        time.sleep(5)
        self.q_city.join()
        self.q_brand.join()
        self.q_district.join()
        self.q_dlr.join()

    def taskleft(self):
        return self.q_city.qsize()+self.q_brand.qsize()+self.running

    def push(self,req):
        self.q_city.put(req)

    def pop(self):
        return self.q_dlr.get()

    def threadget(self):
        while True:
            req = self.q_req.get()
            with self.lock:
                self.running += 1
            try:
                ans = requests.get(req).content
            except Exception as what:
                ans = ''
                print(what)
            self.q_ans.put((req, ans))
            with self.lock:
                self.running -= 1
            self.q_req.task_done()
            time.sleep(0.1)

    def get_proxy(self):
        r = requests.get('http://127.0.0.1:8000/?protocol=0&count=100&country=国内')
        ip_ports = json.loads(r.text)
        proxies = []
        for ip_port in ip_ports:
            ip = ip_port[0]
            port = ip_port[1]
            proxy = {
                'http': 'http://%s:%s' % (ip, port),
            }
            proxies.append(proxy)
        return choice(proxies)

    def get_headers(self):
        headers = []
        for ua in self.USER_AGENT_LIST:
            header = {
                'User-Agent': ua,
                'Referer': 'http://dealer.bitauto.com/beijing/audi/'
            }
            headers.append(header)
        return choice(headers)

    def get_province_info(self):
        url = 'http://auto.sohu.com/dealer/static/provinceArr.js'
        r = requests.get(url)
        province_dict = {}
        provincelist = json.loads(bytes.decode(r.content).split('= ')[1])
        for i in provincelist:
            # print(i)
            province_dict[i['id'][:2]] = i['name'][2:]
        return province_dict

    def get_citylist(self):
        url = 'http://api.admin.bitauto.com/city/getcity.ashx?'
        params = {
            'callback': 'City_Select._$JSON_callback.$JSON',
            'requesttype': 'json',
            'bizCity': 1
        }
        print('正在抓取城市列表，url='+url)
        r = requests.get(url, params=params, headers=self.get_headers())
        citylist = json.loads(bytes.decode(r.content[34:-2]))
        return citylist

    def get_brandlist(self):
        while not self.q_city.empty():
            # with self.lock:
            #     self.running += 1
            city = self.q_city.get()
            print('剩余'+str(self.q_city.qsize()) + '城市')
            url = 'http://api.car.bitauto.com/CarInfo/getlefttreejson.ashx?'
            params = {
                'tagtype': 'jingxiaoshang',
                'pagetype': 'masterbrand',
                'objid': 0,
                'citycode': city['cityPinYin'] + '/',  # 'suzhou/',
                'cityid': city['cityId'],  # 1502
            }
            for i in range(3):
                try:
                    self.count += 1
                    print(self.count,'次请求,抓取品牌信息，url='+url)
                    r = requests.get(url, params=params, headers=self.get_headers(), proxies=self.get_proxy(), timeout=1.5)
                    break
                except Exception as e:
                    print("fetch %s  failed!\n%s , retry %d" % (url, str(e), i))
                    time.sleep(1)
                    r = ''
                    continue
            if r == '':
                continue
            brandstr = bytes.decode(r.content[14:-1])
            p1 = re.compile(r'id:(\d+)')
            p2 = re.compile(r'name:"(.+?)"')
            p3 = re.compile(r'url:"(.+?)"')
            p4 = re.compile(r'num:(\d+)')
            id = re.findall(p1, brandstr)
            name = re.findall(p2, brandstr)
            url = re.findall(p3, brandstr)
            num = re.findall(p4, brandstr)
            brandlist = []
            for i, na, u, nu in zip(id, name, url, num):
                brand = {
                    'id': i,
                    'name': na,
                    'url': u,
                    'num': nu,
                    'regionid': city['regionId'],
                    'city': city['regionName'],
                    'province': self.provincedict[city['parentId'][:2]]
                }
                # brandlist.append(brand)
                # print(brand)
                self.q_brand.put(brand)
            # with self.lock:
            #     self.running -= 1
            # self.q_city.task_done()
            time.sleep(1)
        # return brandlist

    def get_district(self):
        while not self.q_brand.empty():
            brand = self.q_brand.get()
            print('品牌数量'+str(self.q_brand.qsize()))
            # with self.lock:
            #     self.running += 1
            suburl = brand['url']
            url = 'http://dealer.bitauto.com'
            for i in range(3):
                try:
                    self.count += 1
                    print(self.count,'次请求,抓取分区信息，url:'+url+suburl)
                    r = requests.get(url + suburl, headers=self.get_headers(), proxies=self.get_proxy(), timeout=1.5)
                    break
                except Exception as e:
                    print("fetch %s  failed!\n%s , retry %d" % (url+suburl, str(e), i))
                    time.sleep(1)
                    continue
            try:
                html = etree.HTML(bytes.decode(r.content))
            except Exception as e:
                print('error')
                continue
            # 直辖市要区分
            if brand['regionid'] in ['110100', '120100', '500100', '310100']:
                href = html.xpath('//dl[@id="cityarea"]//a/@href')
                district = html.xpath('//dl[@id="cityarea"]//a/text()')

            else:
                href = html.xpath('//div[@class="area-sub"]//a/@href')
                district = html.xpath('//div[@class="area-sub"]//a/text()')
            for h, d in zip(href, district):
                districtdict = {
                    'href': h,
                    'name': d,
                    'brand': brand['name'],
                    'city': brand['city'],
                    'province': brand['province'],
                }
                # districtlist.append(districtdict)
                self.q_district.put(districtdict)
            # with self.lock:
            #     self.running -= 1
                # self.q_brand.task_done()
            time.sleep(2)
            # if len(districtlist) != 0:
            #     print(districtlist)
            #     return districtlist

    def get_dlrinfo(self):
        while not self.q_district.empty():
            district = self.q_district.get()
            print('分区数量'+str(self.q_district.qsize()))
            # with self.lock:
            #     self.running += 1
            suburl = district['href']
            url = 'http://dealer.bitauto.com'
            for i in range(3):
                try:
                    self.count += 1
                    print(self.count,'次请求,抓取dlr信息，url:'+url+suburl)
                    r = requests.get(url + suburl, headers=self.get_headers(), proxies=self.get_proxy(), timeout=1.5)
                    break
                except Exception as e:
                    print("fetch %s  failed!\n%s , retry %d" % (url+suburl, str(e), i))
                    time.sleep(1)
                    continue
            try:
                html = etree.HTML(bytes.decode(r.content))
            except:
                print('解析页面失败！')
                continue
            for dlr in html.xpath('//div[@class="row dealer-list"]'):
                dealer = {
                    'category': dlr.xpath('.//h6/a/em/text()')[0],
                    'name': dlr.xpath('.//h6/a/text()')[0],
                    'brand': district['brand'],
                    'id': dlr.xpath('.//p[@class="tel"]/span[2]/@id')[0],
                    'address': dlr.xpath('.//p[@class="add"]/span[2]/@title')[0],
                    'district': district['name'],
                    'city': district['city'],
                    'province': district['province'],
                    'brand-info': dlr.xpath('.//p[@class="brand"]/text()')[0],
                }
                # print(dealer)
                # dealer_list.append(dealer)
                self.q_dlr.put(dealer)
                print('经销商数量'+str(self.q_dlr.qsize()))
            # with self.lock:
            #     self.running -= 1
            # self.q_district.task_done()
            time.sleep(2)
        return

    def save_as_csv(self):
        with open('yiche20180122.csv', 'w', newline='') as f:
            w = csv.writer(f)
            w.writerow(['category','name','brand','id','address','district','city','province','brand-info'])
            while not self.q_dlr.empty():
                dlr = self.q_dlr.get()
                print('正在写入经销商'+dlr['id'])
                try:
                    w.writerow(dlr.values())
                except Exception as e:
                    print('写入失败,%s' % str(e))
                    continue

    def run(self):
        citys = self.get_citylist()
        for city in citys:
            self.push(city)
        # print(str(self.q_city.qsize())+'城市数量')
        threads = []
        for i in range(1):
            t = Thread(target=self.get_brandlist)
            # t.setDaemon(True)
            t.start()
            threads.append(t)
            # print(str(self.running)+'个任务')
        time.sleep(5)
        # print('品牌数量'+str(self.q_brand.qsize()))

        for i in range(20):
            t = Thread(target=self.get_district)
            # t.setDaemon(True)
            t.start()
            threads.append(t)
            # print(str(self.running)+'个任务')
        time.sleep(10)
        # print('分区数量'+str(self.q_district.qsize()))
        for i in range(8):
            t = Thread(target=self.get_dlrinfo)
            # t.setDaemon(True)
            t.start()
            threads.append(t)
            # print(str(self.running)+'个任务')
        # print('经销商数量'+str(self.q_dlr.qsize()))
        print(len(threads))
        # [thread.start() for thread in threads]
        [thread.join() for thread in threads]
        # self.q_city.join()
        # self.q_brand.join()
        # self.q_district.join()

        # while self.running:
        #     print(self.q_city.get())
        #     print(self.q_brand.get())
        #     print(self.q_district.get())
        #     print(self.q_dlr.get())
            # print(self.q_city.get())
        self.save_as_csv()


if __name__ in "__main__":
    f = Fetcher(threads = 10)
    f.run()

    # while f.taskleft():
    #     url, content = f.pop()
    #     print(url, len(content))