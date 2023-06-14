# AutoDealerSpider
爬取各汽车品牌官网的经销商信息，抓取的主要字段有经销商代码，省份，城市，县区，品牌，名称，地址，联系电话，坐标等


## 1. 各品牌完成情况

 | 品牌 | 简称 | 爬虫 | 状态 | 备注 |
| --------   | -----  | ---- |--------   | -----  | 
| 别克 | Buick | BuickSpider | OK |  |
| 比亚迪 | Byd | BydSpider | OK |  |
| 长安汽车 | Changan | ChanganSpider | OK |  |
| 雪佛兰 | Chevrolet | ChevroletSpider | OK |  |
| 东风雪铁龙 | Dfcitroen | DfcitroenSpider | OK | POST |
| 一汽大众 | Fawvm | FawvmSpider | OK |  |
| 长安福特 | Ford | FordSpider | OK |  |
| 一汽丰田 | Ftms | FtmsSpider | OK | POST |
| 广汽丰田 | Gactoyota | GactoyotaSpider | OK |  |
| 吉利汽车 | Geely | GeelySpider | OK |  |
| 广汽本田 | Ghac | GhacSpider | OK |  |
| 东风本田 | Honda | HondaSpider | OK | POST |
| 北京现代 | Hyundai | HyundaiSpider | OK | 类似广汽丰田 |
| 东风悦达起亚 | Kia | KiaSpider | OK |  |
| 东风日产 | Nissan | NissanSpider | OK | POST |
| 东风标致 | Peugeot | PeugeotSpider | OK |  |
| 斯柯达 | Skoda | SkodaSpider | OK |  |
| 上汽大众 | Svm | SvmSpider | OK |  |
| WEY | Wey | WeySpider | OK |  |
| 哈弗 | Haval | HavalSpider | NG | POST，网址编码问题，post请求问题 |
| DS | Ds | DsSpider | DELETE |  |


## 2. 使用

### 安装相关库
```bash
# pip安装scrapy， pandas， requests
>pip install -U -i https://pypi.tuna.tsinghua.edu.cn/simple pip
>pip install -i https://pypi.tuna.tsinghua.edu.cn/simple scrapy  
>pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pandas
>pip install -i https://pypi.tuna.tsinghua.edu.cn/simple requests  

```

### 快速导出数据
```bash
# 列出所有爬虫
>scrapy list

# 运行指定爬虫,导出数据为csv格式
>scrapy crawl byd -o byd.csv

# 上述csv文件用Excel可能打不开，可使用cache目录下的csv2xlsx.py转化格式（需安装pandas库）
>python csv2xlsx.py byd.csv

```
### 批量运行爬虫
运行runspider.py即可批量运行爬虫，数据会存在Data目录下
```bash
python runspider.py
```

### 使用百度API补充县区数据的pipelines

修改pipelines.py文件
```python
import requests
import logging
class AddressPraser(object):

    def __init__(self):
        self.s = requests.Session()
        self.ak = '****'
        self.translate_api = 'http://api.map.baidu.com/geoconv/v1/?coords={}&from=5&to=6&ak={}'
        self.poi_api = 'http://api.map.baidu.com/?qt=rgc&x={}&y={}&dis_poi=100&poi_num=10&' \
                  'latest_admin=1&ak={}'

    def process_item(self, item, spider):
        if (item['县区'] == '') and item['坐标'] :
            r = self.s.get(self.translate_api.format(item['坐标'], self.ak),)
            xy = r.json()['result'][0]
            r = self.s.get(self.poi_api.format(xy['x'], xy['y'], self.ak),)
            address =  r.json()['content']
            item['县区'] = address['address_detail']['district']
            if item['地址'] == '':
                item['地址'] = address['address']
            print('地址处理：', item)
            logging.info('地址处理：'+str(item))
            return item
        else:
            return item

    def close_spider(self, spider): #关闭爬虫时
        pass
```

### 使用导出为Excel的pipelines

修改pipelines.py文件
```python
from datetime import date
import pandas as pd
class ExportToXlsx(object):

    def __init__(self):
        self.path = 'Data'
        self.data = pd.DataFrame()
        self.today = date.strftime(date.today(), '%Y%m%d')

    def process_item(self, item, spider):
        df = pd.DataFrame([item,])
        self.data = pd.concat([self.data, df])
        return item

    def close_spider(self, spider):#关闭爬虫时
        if self.path != '.':
            import os
            os.makedirs(self.path, 777, 1)
        filename = '{}/{}_{}.xlsx'.format(self.path, spider.name, self.today )
        self.data.to_excel(filename, index=None)
```

### 启用重复值的pipelines
```python
from scrapy.exceptions import DropItem
class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['编号'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['编号'])
            return item
```
### 启用上述pipelines

修改settings.py文件启用上述Pipeline
```python
ITEM_PIPELINES = {
        # 'AutoDealerSpider.pipelines.AutodealerspiderPipeline': 300,
        'AutoDealerSpider.pipelines.DuplicatesPipeline': 301,
        'AutoDealerSpider.pipelines.ExportToXlsx': 310,
        'AutoDealerSpider.pipelines.AddressPraser': 303,

}
```
