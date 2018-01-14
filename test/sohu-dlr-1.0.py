import requests
from lxml import etree
import json

url = 'http://dealer.auto.sohu.com/map/?city=320100&brandId=191'

header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
    'Referer':'http://dealer.auto.sohu.com/map/?city=320100'
}

post_data = {
    'lastSelect':["A",191,"0","0"],
    'userSelect':["b191"],
    'lastMode': 1
}
r = requests.post(url,data=post_data, headers=header )
# print(r.content)
html = etree.HTML(bytes.decode(r.content))
print(html.xpath('//script[2]/text()'))
data = html.xpath('//script[2]/text()')

dlrlist = json.loads(data[0].split('\n')[1][22:-2])

for dlr in dlrlist:
    print(dlr)

