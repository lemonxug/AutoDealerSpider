# -*- coding: utf-8 -*-

import requests
import json
import csv

# url = 'http://www.dyk.com.cn/public/dyk/js/allDealersData.js'
#
# r=requests.post(url)
#
# dlr_dict = json.loads(bytes.decode(r.content)[18:])  # 生成字典
# print(dlr_dict['110000'])
#
# with open('dyk.json', 'w') as f:
#     j_dlr_dict = json.dumps(dlr_dict)   # 转换成字符串
#     f.write(j_dlr_dict)    # 写入文件


# print(r.content)
with open('dyk.json', 'r') as f:   #
    dlr = json.load(f)
    # print(type(dlr))
    # print(dlr['110000'][1]['id'])
list_list=[]

with open('test.csv','w',encoding='gbk') as f:  # 指定文件的编码
    w = csv.writer(f)
    w.writerow(dlr['110000'][1].keys())
    for key,value in dlr.items():
        for item in value:
            # for k, v in item.items():
            #     try :
            #         v.replace(u'\xa0', u' ')
            #         v.encode('gbk', u'\xa0')
            #         k.replace(u'\xa0', u' ')  # 替换不能编码的字符
            #     except:
            #         pass
            # w.writerow(item.keys())
            # w.writerow(item.values())
            # print(type(item))
            for k, v in item.items():
                if not v:
                    item[k] = 'None'  # 空值赋值‘None’
            w.writerow(item.values())
            # print(key,item.keys(),item.values())

# print(le (dlr['110000'][1]))

