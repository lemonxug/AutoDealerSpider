# -*- coding: utf-8 -*-

# Scrapy settings for AutoDealerSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'AutoDealerSpider'

SPIDER_MODULES = ['AutoDealerSpider.spiders']
NEWSPIDER_MODULE = 'AutoDealerSpider.spiders'

LOG_FILE = 'crawl.log'
LOG_ENABLED = True

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

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'AutoDealerSpider (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.5
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/'
                      '537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'AutoDealerSpider.middlewares.AutodealerspiderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'AutoDealerSpider.middlewares.AutodealerspiderDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
        # 'AutoDealerSpider.pipelines.AutodealerspiderPipeline': 300,
        'AutoDealerSpider.pipelines.DuplicatesPipeline': 301,
        'AutoDealerSpider.pipelines.ExportToXlsx': 310,
        'AutoDealerSpider.pipelines.AddressPraser': 303,

}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
