# coding=utf-8
import json
import pandas as pd
from DemoSpider import DemoSpider
import requests
from urllib import parse


name = '长安福特'
url = 'http://www.ford.com.cn/api/dealer.aspx'  # 长安福特


class FordSpider(DemoSpider):


    def __init__(self):
        self.url = url
        self.name = name

    def prase_response(self, r):
        try:
            print('正在处理'+self.name+'经销商信息。。。')
            dlr_list = []
            url = 'https://www.ford.com.cn/content/ford/cn/zh_cn/configuration/application-and-services-config/provinceCityDropDowns.multiFieldDropdown.data'
            r = requests.get(url)
            # print(r.content)
            province_list = json.loads(bytes.decode(r.content))
            for p in province_list:
                # print(p['provinceKey'])
                for c in p['cityList']:
                    # file_url = parse.quote(data['Entity'][5:])
                    # 获取中心经纬度
                    url = 'https://restapi.amap.com/v3/geocode/geo?key=1891d0f847c0a210a88015fdd4c3bc46&s=rsv3&callback=jsonp_232&platform=JS&logversion=2.0&sdkversion=1.3&appname=http://www.ford.com.cn/dealer/locator?intcmp=hp-return-fd&csid=D6C889F7-2FF1-4EA5-8D60-494D42872518&' + \
                          'address=' + parse.quote(p['provinceKey']) + \
                          parse.quote(c['cityKey']) \
                        # +'&callback=jsonp_232&_=1510383274081'
                    r = requests.get(url)
                    # print(r.content)
                    tmp = json.loads(bytes.decode(r.content)[10:-1])
                    url = 'https://yuntuapi.amap.com/datasearch/around?s=rsv3&key=1891d0f847c0a210a88015fdd4c3bc46&extensions=base&language=en&enc=utf-8&output=jsonp&sortrule=_distance:1&keywords=&limit=100&tableid=55adb0c7e4b0a76fce4c8dd6&radius=35000&callback=jsonp_333&platform=JS&logversion=2.0&sdkversion=1.3&appname=http://www.ford.com.cn/dealer/locator?intcmp=hp-return-fd&csid=C0F2C0C7-D2A2-4730-9618-5B2C060C3DDD&' + \
                          'center=' + tmp['geocodes'][0]['location'] + \
                          '&filter=AdministrativeArea:' \
                          + parse.quote(p['provinceKey']) \
                          + ' Locality:' \
                          + parse.quote(c['cityKey'])

                    r = requests.get(url)
                    # print(r.content)
                    tmp = json.loads(bytes.decode(r.content)[10:-1])
                    # print(tmp)
                    for dlr in tmp['datas']:
                        # print(dlr)
                        dealer = {
                            '编号': dlr['DealerID'],
                            '省份': dlr['_province'],
                            '城市': dlr['_city'],
                            '县区': dlr['_district'],
                            '品牌' : self.name,
                            '公司名称':dlr['_name'],
                            '联系电话':dlr['ServicePhoneNumber'],
                            '地址':dlr['_address'],
                            '经度':dlr['_location'].split(',')[0],
                            '纬度':dlr['_location'].split(',')[1],
                            '坐标':dlr['_location'],
                            '分类':dlr['DealerAffiliation'],
                        }
                        print(dealer)
                        dlr_list.append(dealer)

            dlrs = pd.DataFrame(dlr_list)
            self.dlrs = dlrs[['编号','省份','城市','县区','品牌','公司名称','联系电话','地址','经度','纬度','坐标', '分类']]
        except Exception as e:
            raise e


if __name__ == '__main__':
    s = FordSpider()
    s.run()
