

class PeugeotSpider():

    def prase_request(self):
        dlr_dict = {}
        session = requests.session()
        cookies = {}
        with open('cookies', 'r') as f:
            for line in f.read().split(';'):
                name, value = line.strip().split('=', 1)
                cookies[name] = value  # 为字典cookies添加内容
        # print(parse.unquote(cookies['dealer_province_name']))
        # print(cookies['dealer_province_id'])
        r = session.get(self.js_url, cookies=cookies)
        html = etree.HTML(bytes.decode(r.content))
        for province in html.xpath('//div[@class="cityGroup"]'):
            # print(province.xpath('./div/text()')[0])
            for city in province.xpath('.//a'):
                # print(city.xpath('./text()')[0])
                # print(city.xpath('string(.)'))
                # print(city.xpath('./@*')[1].split('(\'')[1][:-2])
                cookies['dealer_province_name'] = parse.quote(city.xpath('./text()')[0])
                cookies['dealer_province_id'] = city.xpath('./@*')[1].split('(\'')[1][:-2] # string
                r = session.get(self.js_url, cookies=cookies)
                html = etree.HTML(bytes.decode(r.content))
                time.sleep(1)
                for dlr in html.xpath('//div[@class="col-xs-12 col-sm-3 searchCResult"]'):
                #     print(dlr)
                    try:
                        dealer = {
                            'name': dlr.xpath('.//span[@class="result_right searchRNam"]/text()')[0],
                            'address':dlr.xpath('.//span[@class="result_right"]/text()')[0],
                            'tel': dlr.xpath('.//span[@class="result_right"]/text()')[1],
                            'city':city.xpath('./text()')[0],
                            'province':province.xpath('./div/text()')[0],
                        }
                        # print(dealer)
                        dlr_dict[dealer['tel']] = dealer
                    except:
                        print(province.xpath('./div/text()')[0], city.xpath('./text()')[0])
                        # print(dlr.xpath('string(.)'))
        return dlr_dict

peugeot_url = 'http://dealer.peugeot.com.cn/finddealer.php#carInfoNav'  # 东风标致 - doing
peugeot = PeugeotSpider('东风标致', 'peugeot', peugeot_url)