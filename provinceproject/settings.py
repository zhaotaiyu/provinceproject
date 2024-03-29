# -*- coding: utf-8 -*-

# Scrapy settings for provinceproject project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'provinceproject'

SPIDER_MODULES = ['provinceproject.spiders']
NEWSPIDER_MODULE = 'provinceproject.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'

# Obey robots.txt rules
#ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#     'Connection': 'keep-alive',
#     'Cache-Control': 'max-age=0',
#     'Origin': 'http://dn4.gxzjt.gov.cn:1141',
#     'Upgrade-Insecure-Requests': '1',
#     'Content-Type': 'application/x-www-form-urlencoded',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
#     'Referer': 'http://dn4.gxzjt.gov.cn:1141/WebInfo/Enterprise/Enterprise.aspx',
#     'Accept-Encoding': 'gzip, deflate',
#     'Accept-Language': 'zh-CN,zh;q=0.9',
# }


# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'provinceproject.middlewares.ProvinceprojectSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   #'provinceproject.middlewares.MyUseragent': 542,
   #'provinceproject.middlewares.AbuyunProxyMiddleware': 543,
   #'provinceproject.middlewares.KuaidailiMiddleware': 544,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    # 'provinceproject.pipelines.CeshiPipeline': 209,
    'provinceproject.pipelines.ProvinceprojectPipeline': 300,
    'provinceproject.pipelines.PgsqlPipeline': 301,
    # 'provinceproject.pipelines.ScrapyKafkaPipeline': 302,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
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
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
#LOG_LEVEL= 'ERROR'
LOG_LEVEL= 'DEBUG'
#PGSQL
PGSQL_URI="ecs-a025-0002"
PGSQL_DATABASE="cic_database"
PGSQL_PASS="sikuyi"
PGSQL_USER="postgres"
PGSQL_PORT=54321

#SCRAPY配置
#DOWNLOAD_TIMEOUT=100
RETRY_HTTP_CODES = [500, 502, 503, 504, 400, 403, 408, 429, 407]
RETRY_TIMES = 10
HTTPERROR_ALLOWED_CODES = [301,302, 500, 502, 503, 504, 400, 403, 408, 429, 407]
#abuyun代理配置
PROXYUSER="HR58I089C2G8N57D"
PROXYPASS="3EB3D83115080960"
PROXYSERVER="http://http-dyn.abuyun.com:9020"
#MONGO配置
MONGOCLIENT='mongodb://ecs-a025-0002:27017/'
MONGODATABASE='error'
MONGOTABLE='province'
#快代理配置
KUAI_USERNAME="zhao_tai_yu"
KUAI_PASSWORD="7av2i9t5"

#KAFKA配置
BOOTSTRAP_SERVER="49.4.90.247:6667"
TOPIC="TOPIC_sikuyifinally"