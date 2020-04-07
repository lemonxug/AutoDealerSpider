
1. 品牌列表
厂商，品牌，，英文简称，域名，爬虫，备注

2. 生成爬虫 
scrapy gensipder <name> <domian>

爬取字段
省份，地市，县区，品牌，名称

# 问题记录
1. 执行系统命令
> https://blog.csdn.net/luckytanggu/article/details/51793218

```python
# 1.os.system
import os
os.system('date')

# 2.os.popen
import os
nowtime = os.popen('date')
print nowtime.read()

# 3.commands
import commands
status, output = commands.getstatusoutput('date')
print(status)    # 0
print(output)    # 2016年 06月 30日 星期四 19:26:21 CST

# 4.subprocess
import subprocess
nowtime = subprocess.Popen('date', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
print(nowtime.stdout.read())
```
2. POST请求的参数问题
>https://www.cnblogs.com/qiaoer1993/p/11384679.html
```python
# scrapy.Request，formdata必须得是字符串，如果是表单格式，那么需要用json.dumps()转为字符串格式
# scrapy.Request(url=url,method="POST",body=formdata,cookies=self.cookie,headers=self.headers,callback=self.get_goods_list)

# scrapy.FormRequest，formdata是dict格式
# scrapy.FormRequest(url=url,formdata=formdata,cookies=self.cookie,headers=self.headers,callback=self.get_goods_list)

# requests，data用的必须是字符串类型，json用的是dict格式
# requests.post(url, data=json.dumps(formdata))
# requests.post(url, json=formdata)
```


## BYD
http://www.bydauto.com.cn/sites/custom/service/auto/sales?type=getBeforeSaleProvinces&carType=%E5%AE%8BPro
http://www.bydauto.com.cn/sites/custom/service/auto/sales?type=getBeforeSaleCitys&carType=%E5%AE%8BPro&province=%E5%AE%89%E5%BE%BD
http://www.bydauto.com.cn/sites/custom/service/auto/sales?type=getBeforeSaleStores&carType=%E5%AE%8B%E7%BB%8F%E5%85%B8%E7%89%88&province=%E9%87%8D%E5%BA%86&city=%E9%87%8D%E5%BA%86

## beijing-hyundai
https://www.beijing-hyundai.com.cn/umbraco/surface/Common/GetProvinces
https://www.beijing-hyundai.com.cn/umbraco/surface/Common/GetCitys
https://www.beijing-hyundai.com.cn/umbraco/surface/Common/GetDealers?tag=

## dfcitroen
http://www.dongfeng-citroen.com.cn/4s/index.php/dsearch
http://www.dongfeng-citroen.com.cn/4s/index.php/api/getCities/2
http://www.dongfeng-citroen.com.cn/4s/index.php/api/getDealersByLocation

## ford
https://www.ford.com.cn/content/ford/cn/zh_cn/configuration/application-and-services-config/vehicle-list.dropdownChina.data
https://www.ford.com.cn/content/ford/cn/zh_cn/configuration/application-and-services-config/provinceCityDropDowns.multiFieldDropdownChina.data
https://restapi.amap.com/v3/geocode/geo?key=1891d0f847c0a210a88015fdd4c3bc46&s=rsv3&callback=jsonp_232&platform=JS&logversion=2.0&sdkversion=1.3&appname=http://www.ford.com.cn/dealer/locator?intcmp=hp-return-fd&csid=D6C889F7-2FF1-4EA5-8D60-494D42872518&address=%E6%B1%9F%E8%8B%8F%E8%8B%8F%E5%B7%9E&callback=jsonp_232&_=1585631071515
https://yuntuapi.amap.com/datasearch/local?s=rsv3&key=1891d0f847c0a210a88015fdd4c3bc46&extensions=all&language=en&enc=utf-8&output=jsonp&&sortrule=_distance:1&autoFitView=true&panel=result&keywords=&limit=100&sortrule=_id:1&tableid=55adb0c7e4b0a76fce4c8dd6&radius=50000&platform=JS&logversion=2.0&sdkversion=1.4.2&appname=http://www.ford.com.cn/dealer/locator?intcmp=hp-return-fd&csid=6F094767-5285-454B-BC73-0D18F9C7223B&center=120.585315,31.298886&city=%E8%8B%8F%E5%B7%9E&filter=AdministrativeArea:%E6%B1%9F%E8%8B%8F&callback=jsonp_333&_=1585631071516

## honda
http://www.dongfeng-honda.com/dot_query.shtml
http://www.dongfeng-honda.com/index/get_city_bypid/1369
http://www.dongfeng-honda.com/index.php/Index/get_dealer_by_city

## dongfeng-nissan
https://api.dongfeng-nissan.com.cn/api/Nissan/GetNissanCity
https://www.dongfeng-nissan.com.cn/Nissan/ajax/Distributor/GetJsonDistributorList

## peugeot
http://dealer.peugeot.com.cn/dealertype.js?v20311525

## haval
https://mall.haval.com.cn/area/returnPlaceId.html?province=%25E9%2587%258D%25E5%25BA%2586&city=%25E9%2587%258D%25E5%25BA%2586
https://mall.haval.com.cn/cars/getDealerByType.html

## wey
https://www.wey.com/index.php?m=tiyan&c=index&a=province
https://www.wey.com/index.php?m=tiyan&c=index&a=distributor&b=%E7%9B%90%E5%9F%8E%E5%B8%82&t=

