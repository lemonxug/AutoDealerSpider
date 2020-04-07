
import os

BRANDS = [
        {'name-en':'Buick', 'domain':'buick.com.cn', 'name':'别克',},
        {'name-en':'Byd', 'domain':'bydauto.com.cn', 'name':'比亚迪',},
        {'name-en':'Changan', 'domain':'changan.com.cn', 'name':'长安汽车',},
        {'name-en':'Chevrolet', 'domain':'mychevy.com.cn', 'name':'雪佛兰',},
        {'name-en':'Dfcitroen', 'domain':'dongfeng-citroen.com.cn', 'name':'东风雪铁龙',},
        {'name-en':'Kia', 'domain':'dyk.com.cn', 'name':'东风悦达起亚',},
        {'name-en':'Fawvm', 'domain':'faw-vw.com', 'name':'一汽大众',},
        {'name-en':'Ford', 'domain':'ford.com.cn', 'name':'长安福特',},
        {'name-en':'Ftms', 'domain':'ftms.com.cn', 'name':'一汽丰田',},
        {'name-en':'Gactoyota', 'domain':'gac-toyota.com.cn', 'name':'广汽丰田',},
        {'name-en':'Geely', 'domain':'geely.com', 'name':'吉利汽车',},
        {'name-en':'Ghac', 'domain':'ghac.cn', 'name':'广汽本田',},
        {'name-en':'Wey', 'domain':'wey.com', 'name':'WEY',},
        {'name-en':'Haval', 'domain':'haval.cn', 'name':'哈弗',},
        {'name-en':'Honda', 'domain':'dongfeng-honda.com', 'name':'东风本田',},
        {'name-en':'Hyundai', 'domain':'beijing-hyundai.com.cn', 'name':'北京现代',},
        {'name-en':'Nissan', 'domain':'dongfeng-nissan.com.cn', 'name':'东风日产',},
        {'name-en':'Peugeot', 'domain':'peugeot.com.cn', 'name':'东风标致',},
        {'name-en':'Skoda', 'domain':'skoda.com.cn', 'name':'斯柯达',},
        {'name-en':'Svm', 'domain':'svw-volkswagen.com', 'name':'上汽大众',},
        {'name-en':'Ds', 'domain':'ds.com.cn', 'name':'DS',},
]


if __name__ == '__main__':
    print(os.getcwd())
    for b in BRANDS:
        # print('scrapy genspider {} {}'.format(b['name-en'].lower(), b['domain']))
        # t = os.popen('scrapy genspider {} {}'.format(b['name-en'].lower(), b['domain']))
        # print(t.read())
        # print('{}Spider'.format(b['name-en']))
        print(b['name'])