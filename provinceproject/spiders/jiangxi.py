# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from provinceproject.items import *
import datetime
class JiangxiSpider(scrapy.Spider):
    name = 'jiangxi'
    #allowed_domains = ['59.52.254.106:8093/qualificationCertificateListForPublic']
    start_urls = ['http://59.52.254.106:8093/qualificationCertificateListForPublic/']
    def start_requests(self):
        url='http://59.52.254.106:8093/qualificationCertificateListForPublic?pageIndex={}&enterpriseLevel=&enterpriseName=&legalRepresentative=&certificateNum=&registrationNum='
        for page in range(1,1414):
            page_url=url.format(str(page))
            yield Request(page_url,callback=self.parse)
    def parse(self, response):
        tr_list=response.xpath("//tr[@class='tr_change']")
        if tr_list:
            for tr in tr_list:
                company_url=tr.xpath("./td[3]/a/@onclick").extract_first()
                if company_url:
                    company_url="http://59.52.254.106:8093"+company_url.split("'")[1]
                    yield Request(company_url,callback=self.parse_company)
    def parse_company(self,response):
        jiangxi=JiangxiItem()
        jiangxi["id"] = response.url.split("=")[-1]
        jiangxi["name"] = str(response.xpath("//table[@class='addProjectTable siteFrome_info']/tr[1]/td[2]/text()").extract_first()).strip()
        jiangxi["leal_person"] = str(response.xpath("//table[@class='addProjectTable siteFrome_info']/tr[2]/td[2]/text()").extract_first()).strip()
        jiangxi["address"] = str(response.xpath("//table[@class='addProjectTable siteFrome_info']/tr[3]/td[2]/text()").extract_first()).strip()
        jiangxi["social_credit_code"] = str(response.xpath("//table[@class='addProjectTable siteFrome_info']/tr[4]/td[2]/text()").extract_first()).strip()
        jiangxi["regis_type"] = str(response.xpath("//table[@class='addProjectTable siteFrome_info']/tr[5]/td[2]/text()").extract_first()).strip()
        jiangxi["registered_capital"] = str(response.xpath("//table[@class='addProjectTable siteFrome_info']/tr[6]/td[2]/text()").extract_first()).strip("\r\n\t人民币").replace(",","")
        jiangxi["lic_num"] = str(response.xpath("//table[@class='addProjectTable siteFrome_info']/tr[7]/td[2]/text()").extract_first()).strip()
        jiangxi["lic_useful_date"] = str(response.xpath("//table[@class='addProjectTable siteFrome_info']/tr[8]/td[2]/text()").extract_first()).strip()
        jiangxi["lic_organ"] = str(response.xpath("//table[@class='addProjectTable siteFrome_info']/tr[9]/td[2]/text()").extract_first()).strip()
        jiangxi["url"] = response.url
        jiangxi["create_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        jiangxi["modification_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        jiangxi["is_delete"] = 0
        tr_list=response.xpath("//table[@class='listTable hoverTable trbgTable detailPopupTable']/tbody/tr")
        if tr_list:
            for tr in tr_list:
                jiangxi["aptitude_level"] = tr.xpath("./td[2]/text()").extract_first()
                jiangxi["aptitude_type"] = tr.xpath("./td[3]/text()").extract_first()
                jiangxi["check_time"] = tr.xpath("./td[4]/text()").extract_first()
                yield jiangxi
