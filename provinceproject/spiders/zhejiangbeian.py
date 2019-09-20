# -*- coding: utf-8 -*-
import datetime
import re
import scrapy
import pymongo
from scrapy import Request
from ..settings import *
from provinceproject.items import BeianItem

class ZhejiangbeianSpider(scrapy.Spider):
    name = 'zhejiangbeian'
    #allowed_domains = ['223.4.65.131:8080/jzba.php?p=1']
    #start_urls = ['http://223.4.65.131:8080/jzba.php?p=1&State=%E5%AE%A1%E6%A0%B8%E9%80%9A%E8%BF%87']
    custom_settings = {
        'DOWNLOAD_DELAY': '0.2',
        'DOWNLOADER_MIDDLEWARES':{'provinceproject.middlewares.AbuyunProxyMiddleware': 543,}
    }
    def start_requests(self):
        url='http://223.4.65.131:8080/jzba.php?p=1&State=%E5%AE%A1%E6%A0%B8%E9%80%9A%E8%BF%87'
        yield Request(url,callback=self.parse,meta={'dont_redirect':True})
    def parse(self, response):
        total_page = int(re.findall(".*?(\d+).*", response.xpath("//div[@class='page_control']/div[1]/table/tr/td[1]/text()[2]").extract_first())[0])
        for page in range(1, total_page):
            url = "http://223.4.65.131:8080/jzba.php?p={}&State=审核通过".format(page)
            yield Request(url, callback=self.parse_beian,meta={'dont_redirect':True})
    def parse_beian(self, response):
        tr_list = response.xpath("//table[@class='t1']/tr")
        if tr_list:
            for tr in tr_list[1:]:
                beian = BeianItem()
                beian["corpname"] = tr.xpath("./td[2]/div/text()").extract_first()
                beian["corpcode"] = tr.xpath("./td[3]/text()").extract_first()
                beian["record_province"] = "浙江"
                beian["create_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                beian["modification_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                beian["is_delete"] = 0
                yield beian
        else:
            myclient = pymongo.MongoClient('mongodb://ecs-a025-0002:27017/')
            mydb = myclient[MONGODATABASE]
            mycol = mydb[MONGOTABLE]
            mydict = {"url": response.url, "reason": "该页未返回数据", 'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            mycol.insert_one(mydict)
            myclient.close()

