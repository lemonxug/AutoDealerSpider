import scrapy
import logging
from scrapy.crawler import CrawlerProcess
from AutoDealerSpider.spiders.buick import BuickSpider
from AutoDealerSpider.spiders.byd import BydSpider
from AutoDealerSpider.spiders.changan import ChanganSpider
from AutoDealerSpider.spiders.chevrolet import ChevroletSpider
from AutoDealerSpider.spiders.dfcitroen import DfcitroenSpider
from AutoDealerSpider.spiders.fawvm import FawvmSpider
from AutoDealerSpider.spiders.ford import FordSpider
from AutoDealerSpider.spiders.ftms import FtmsSpider
from AutoDealerSpider.spiders.gactoyota import GactoyotaSpider
from AutoDealerSpider.spiders.geely import GeelySpider
from AutoDealerSpider.spiders.ghac import GhacSpider
from AutoDealerSpider.spiders.honda import HondaSpider
from AutoDealerSpider.spiders.hyundai import HyundaiSpider
from AutoDealerSpider.spiders.kia import KiaSpider
from AutoDealerSpider.spiders.nissan import NissanSpider
from AutoDealerSpider.spiders.peugeot import PeugeotSpider
from AutoDealerSpider.spiders.skoda import SkodaSpider
from AutoDealerSpider.spiders.svm import SvmSpider
from AutoDealerSpider.spiders.wey import WeySpider
from AutoDealerSpider.spiders.haval import HavalSpider



process = CrawlerProcess(settings={
        'ITEM_PIPELINES' : {
        # 'AutoDealerSpider.pipelines.AutodealerspiderPipeline': 300,
        'AutoDealerSpider.pipelines.DuplicatesPipeline': 301,
        'AutoDealerSpider.pipelines.ExportToXlsx': 310,
        'AutoDealerSpider.pipelines.AddressPraser': 302,
                    },
        'LOG_FILE' : 'crawl.log',
        'LOG_ENABLED' : True,
        'DOWNLOAD_DELAY' : 0.5,
        })

spiders = [
                BuickSpider,
                BydSpider,
                ChanganSpider,
                ChevroletSpider,
                DfcitroenSpider,
                FawvmSpider,
                FordSpider,
                FtmsSpider,
                GactoyotaSpider,
                GeelySpider,
                GhacSpider,
                HondaSpider,
                HyundaiSpider,
                KiaSpider,
                NissanSpider,
                PeugeotSpider,
                SkodaSpider,
                SvmSpider,
                WeySpider,
                # HavalSpider, # NG
                ]

if __name__ == '__main__':
    for s in spiders:
        process.crawl(s)
    # process.crawl(ChanganSpider)
    process.start() # the script will block here until all crawling jobs are finished

