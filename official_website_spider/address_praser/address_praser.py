import os
import requests
import pandas as pd
import math
import time


count = 1

def call_baidu_api(coordinate):
    global count
    if count % 50 == 0:
        time.sleep(2)
    if len(coordinate) < 5:
        return
    print('调用百度API', count, '次')
    translate_api = 'http://api.map.baidu.com/geoconv/v1/?coords='+ coordinate + \
                    '&from=5&to=6&ak=ycOGlKcy6nqzLuLuI36sn7sSZRToulkZ'
    r = requests.get(translate_api)
    # print(r.json()['result'][0])
    xy = r.json()['result'][0]
    poi_api = 'http://api.map.baidu.com/?qt=rgc&x='+str(xy['x']) +'&y='+ str(xy['y'])+ \
    '&dis_poi=100&poi_num=10&latest_admin=1&ak=ycOGlKcy6nqzLuLuI36sn7sSZRToulkZ'
    r = requests.get(poi_api)
    count += 1
    # print(r.json()['content']['address_detail']['street'])
    return r.json()['content']['address_detail']


def add_info(coordinate):
    try:
        address_detail = call_baidu_api(coordinate)
        p = address_detail['province']
        c = address_detail['city']
        d = address_detail['district']
        return p, c, d
    except:
        return '','',''

def address_praser(f):
    data = pd.read_excel('../'+f)
    data = data.drop_duplicates(['编号','公司名称'])
    print('根据坐标添加地区信息')
    for i, co in zip(data.index, data['坐标']):
        data.loc[i, '省份1'], data.loc[i, '城市1'], data.loc[i, '县区1'] =add_info(co)
        print(data.loc[i, '品牌'], i, co, data.loc[i,'省份1'], data.loc[i, '城市1'], data.loc[i, '县区1'])

    print('保存到'+f.split('.')[0]+'_1.xlsx')
    data.to_excel(f.split('.')[0]+'_1.xlsx', index=False)


def main():
    for f in os.listdir('../'):
        if '.xlsx' in f:
        # if '雪佛兰_20190530.xlsx' in f:
            print('处理：', f)
            address_praser(f)

def fun():
    for f in os.listdir('./'):
        if '.xlsx' in f:
            data = pd.read_excel(f)
            data = data[['编号','省份1','城市1','县区1','品牌','公司名称','联系电话','地址','经度','纬度','坐标', '分类']]
            data.columns = ['编号','省份','城市','县区','品牌','公司名称','联系电话','地址','经度','纬度','坐标', '分类']
            data.to_excel(f.split('_1.')[0]+'_2.xlsx', index=False)


if __name__ == '__main__':
    main()

