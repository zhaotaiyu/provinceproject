# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random
import base64

class MyUseragent():
    def process_request(self,request,spider):
        USER_AGENT_LIST = [
        'MSIE (MSIE 6.0; X11; Linux; i686) Opera 7.23',
        'Opera/9.20 (Macintosh; Intel Mac OS X; U; en)',
        'Opera/9.0 (Macintosh; PPC Mac OS X; U; en)',
        'iTunes/9.0.3 (Macintosh; U; Intel Mac OS X 10_6_2; en-ca)',
        'Mozilla/4.76 [en_jp] (X11; U; SunOS 5.8 sun4u)',
        'iTunes/4.2 (Macintosh; U; PPC Mac OS X 10.2)',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:5.0) Gecko/20100101 Firefox/5.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:9.0) Gecko/20100101 Firefox/9.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:16.0) Gecko/20120813 Firefox/16.0',
        'Mozilla/4.77 [en] (X11; I; IRIX;64 6.5 IP30)',
        'Mozilla/4.8 [en] (X11; U; SunOS; 5.7 sun4u)'
            ]
        agent = random.choice(USER_AGENT_LIST)
        request.headers['User_Agent'] =agent

class AbuyunProxyMiddleware():
    def __init__(self,proxyuser,proxypass,proxyserver):
        self.proxyuser = proxyuser
        self.proxypass = proxypass
        self.proxyserver = proxyserver
        self.proxyauth = "Basic " + base64.urlsafe_b64encode(bytes((self.proxyuser + ":" + self.proxypass), "ascii")).decode("utf8")
    def process_request(self,request,spider):
        request.meta["proxy"] = self.proxyserver
        request.headers["Proxy-Authorization"] = self.proxyauth
    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            proxyuser=crawler.settings.get("PROXYUSER"),
            proxypass=crawler.settings.get("PROXYPASS"),
            proxyserver=crawler.settings.get("PROXYSERVER"),
        )