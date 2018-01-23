# coding=utf-8
from spider import *
import time
import threading

dyk_url = 'http://www.dyk.com.cn/public/dyk/js/allDealersData.js'
dyk = DykmcSpider('东风悦达起亚', 'dyk', dyk_url)

hyundai_url = 'https://www.beijing-hyundai.com.cn/datacenter/static/js/District.js'
hyundai = HyundaiSpider('北京现代','hyundai', hyundai_url)

fawvw_url = 'http://contact.faw-vw.com/uploadfiles/js/dealer.js'   # 一汽大众
fawvw = FawvmSpider('一汽大众', 'fawvm', fawvw_url)

gwm_url = 'http://www.gwm.com.cn/statics/gwm-cn/js/map/dealersShop.js'    # 长城  换地址了。。。
gwm = GwmSpider('长城', 'gwm', gwm_url)

ds_url = 'http://www.ds.com.cn/web/cn/api/dealers?lang=cn&type=3'    # DS
ds = DsSpider('DS', 'ds', ds_url)

buick_url = 'http://www.buick.com.cn/api/dealer.aspx'     # 别克
buick = BuickSpider('别克','buick', buick_url)

svm_url = 'http://club.svw-volkswagen.com/map/latlng.xml'  # 上汽大众
svm = SvmSpider('上汽大众', 'svm', svm_url)

nissan_url = 'https://www.dongfeng-nissan.com.cn/Ajax/AjaxSupport.ashx'   #  东风日产
nissan = NissanSpider('东风日产', 'nissan', nissan_url)

ghac_url = 'http://www.ghac.cn/js/Official/staticData/p_c_dealers_data.js'  # 广汽本田
ghac = GhacSpider('广汽本田','ghac', ghac_url)

ftms_url = 'http://www.ftms.com.cn/app/dealer'  # 一汽丰田
ftms = FtmsSpider('一汽丰田','ftms', ftms_url)

dfcitroen_url = 'http://www.dongfeng-citroen.com.cn/4s/index.php'  # 东风雪铁龙
dfcitroen = DfcitroenSpider('东风雪铁龙', 'dfcitroen', dfcitroen_url)
#
chevrolet_url = 'http://www.mychevy.com.cn/images/files/indexmap.txt'  # 雪佛兰
chevrolet = ChevroletSpider('雪佛兰', 'chevrolet', chevrolet_url)

# 跳过
peugeot_url = 'http://dealer.peugeot.com.cn/finddealer.php#carInfoNav'  # 东风标致 - doing
peugeot = PeugeotSpider('东风标致', 'peugeot', peugeot_url)

gactoyota_url = 'https://www.gac-toyota.com.cn'  # 广汽丰田
gactoyota = GactoyotaSpider('广汽丰田', 'gactoyota', gactoyota_url)

geely_url = 'http://mall.geely.com/index.php'  # 吉利汽车
geely = GeelySpider('吉利汽车', 'geely', geely_url)

skoda_url = 'http://www.skoda.com.cn/assets/js/apps/dealerdata.js'  # 斯柯达
skoda = SkodaSpider('斯柯达', 'skoda', skoda_url)

ford_url = 'http://www.ford.com.cn/api/dealer.aspx'  # 长安福特
ford = FordSpider('长安福特', 'ford', ford_url)

changan_url = 'http://www.changan.com.cn/api/dealer.aspx'  # 长安汽车
changan = ChanganSpider('长安汽车', 'changan', changan_url)

byd_url = 'http://www.bydauto.com.cn/counter-sellpoint.html'  # 比亚迪
byd = BydSpider('比亚迪', 'byd', byd_url)


soueast_url = 'http://www.soueast-motor.com/content/index/12'  # 东南汽车
soueast = SoueastSpider('东南汽车', 'soueast', soueast_url)

jac_url = 'http://www.soueast-motor.com/content/index/12' # 江淮汽车
jac = JacSpider('江淮汽车', 'jac', jac_url)

# soueast_url = 'http://www.soueast-motor.com/content/index/12'  # 东风风行
# soueast = SoueastSpider('东南汽车', 'soueast', soueast_url)


# honda_url = 'http://www.honda.com.cn/api/dealer.aspx'   # 东风本田  # 跳过，页面是静态的，没有经销商信息
# honda = HondaSpider('honda', honda_url)

spiders = [
    dyk, hyundai, fawvw, ds, buick, svm, nissan, ghac, ftms,
    dfcitroen, peugeot, geely, skoda, ford, byd,
    # honda, changan,  # honda, changan 没做
    # gwm, gactoyota   #  官网变更
]

if __name__ == '__main__':
    # gwm.get_data()
    # gwm.export_data()
    # gactoyota.get_data()
    # gactoyota.export_data()
    soueast.get_data()
    soueast.export_data()
    # start = time.time()
    # threads = []
    # print(len(spiders))
    # for s in spiders:
    #     # s.get_data()
    #     t = threading.Thread(target=s.export_data, name=s.name)
    #     t.start()
    #     threads.append(t)
    #     # s.export_data()
    # [t.join() for t in threads]
    # end = time.time()
    # print('共耗时：%f 秒' % (end-start))