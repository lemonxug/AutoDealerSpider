import requests
import scrapy
import json

cid = 203
url = 'http://www.dongfeng-citroen.com.cn/4s/index.php/api/getDealersByLocation'
# post_data = 'city={}'.format(cid)
post_data = {'city': str(cid)}
# r =requests.post(url, data=json.dumps(post_data))
# r =requests.post(url, data=post_data)
# print(r.text)

print(post_data, json.dumps(post_data), type(json.dumps(post_data)))
# scrapy.Request(url,  method='POST',body=json.dumps(post_data),)
