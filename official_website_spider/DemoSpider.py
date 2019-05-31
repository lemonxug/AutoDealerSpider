# coding=utf-8
import requests
from datetime import *


class DemoSpider(object):

    def __init__(self, url, name):
        self.url = url
        self.name = name

    def prase_request(self, url):
        try:
            print('正在抓取'+self.name+'经销商信息。。。')
            r = requests.get(url)
        except Exception as e:
            print('【无法下载网页】')
            raise e
        return r

    def prase_response(self, r):
        self.dlrs = None

    def to_excel(self):
        if len(self.dlrs) > 0:
            today = date.strftime(date.today(), '%Y%m%d')
            print('正在导出'+self.name+'经销商信息。。。')
            self.dlrs.to_excel('data\\'+self.name+'_'+today+'.xlsx', index=False)
        else:
            print('【没有数据】')
    def run(self):
        r = self.prase_request(self.url)
        self.prase_response(r)
        self.to_excel()


if __name__ == '__main__':
    s = DemoSpider()
    s.run()
