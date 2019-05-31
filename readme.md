# 说明

## 1. 去各汽车品牌官网爬取其经销商的信息，目前的完成情况

 | 品牌 | 优先级 | 爬虫 | 状态 | 
 |--|--|--|--|
 | 东风悦达起亚 | 1 | DykmcSpider | OK | 
 | 北京现代 | 1 | HyundaiSpider | OK | 
 | 一汽大众 | 1 | FawvmSpider | OK | 
 | 长城汽车 | 1 | GwmSpider | NG | 
 | DS | 1 | DsSpider | OK | 
 | 别克 | 1 | BuickSpider | OK | 
 | 上海大众 | 1 | SvmSpider | OK | 
 | 东风日产 | 1 | NissanSpider | OK | 
 | 广汽本田 | 0 | GhacSpider | OK | 
 | 一汽丰田 | 1 | FtmsSpider | OK | 
 | 东风雪铁龙 | 1 | DfcitroenSpider | OK | 
 | 雪佛兰 | 1 | ChevroletSpider | OK | 
 | 东风标致 | 0 | PeugeotSpider |  | 
 | 广汽丰田 | 1 | GactoyotaSpider | OK | 
 | 吉利汽车 | 1 | GeelySpider | OK | 
 | 斯柯达 | 1 | SkodaSpider | OK | 
 | 长安福特 | 1 | FordSpider | OK | 
 | 长安汽车 | 0 | ChanganSpider |  | 
 | 比亚迪 | 1 | BydSpider | OK | 
 | 东南汽车 | 0 | SoueastSpider |  | 
 | 江淮汽车 | 0 | JacSpider |  | 
 | 东风风行 | 0 | FxautoSpider |  | 
 | 东风启辰 | 0 | VenuciaSpider |  | 
 | 东风本田 | 0 | HondaSpider |  | 


## 2. 爬取搜狐汽车，易车网等垂直媒体上的经销商信息

| 品牌 | 爬虫 | 状态 |
|--|--|--|
|汽车之家|  | NG| 
|易车网 |  | NG| 
|爱卡汽车 |  | NG| 


## 3. 使用

run_spider.py用来启动爬虫，爬虫会将抓取的信息导出为Excel文件

抓取的主要字段有经销商代码，省份，城市，县区，品牌，名称，地址，联系电话，坐标，分类等

address_praser.py利用抓取的坐标通过百度地图API获取省份，城市，县区等信息，导出为Excel文件
