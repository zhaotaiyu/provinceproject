# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from provinceproject.items import *
import datetime
class JiangxiSpider(scrapy.Spider):
    name = 'jiangxi'
    custom_settings = {
        'DOWNLOAD_DELAY': '0.1',
        # 'DOWNLOADER_MIDDLEWARES': {'provinceproject.middlewares.AbuyunProxyMiddleware': 543, }
    }
    #allowed_domains = ['59.52.254.106:8093/qualificationCertificateListForPublic']
    start_urls = ['http://59.52.254.106:8093/qualificationCertificateListForPublic']
    def parse(self,response):
        total = int(response.xpath("//div[@class='paging']/span[2]/text()").extract_first())
        yushu = total%10
        if yushu:
            total_page = total//10 + 2
        else:
            total_page = total//10 + 1
        url='http://59.52.254.106:8093/qualificationCertificateListForPublic?pageIndex={}&enterpriseLevel=&enterpriseName=&legalRepresentative=&certificateNum=&registrationNum='
        for page in range(1,total_page):
            page_url=url.format(str(page))
            yield Request(page_url,callback=self.parse_next)
    def parse_next(self, response):
        tr_list=response.xpath("//tr[@class='tr_change']")
        if tr_list:
            for tr in tr_list:
                company_url=tr.xpath("./td[3]/a/@onclick").extract_first()
                if company_url:
                    company_url="http://59.52.254.106:8093"+company_url.split("'")[1]
                    yield Request(company_url,callback=self.parse_company)
    def parse_company(self,response):
        c_info = CompanyInfomortation()
        c_info["province_company_id"] = "jiangxi_" + response.url.split("=")[-1]
        c_info["company_name"] = str(response.xpath("//table[@class='addProjectTable siteFrome_info']/tr[1]/td[2]/text()").extract_first()).strip()
        c_info["leal_person"] = str(response.xpath("//table[@class='addProjectTable siteFrome_info']/tr[2]/td[2]/text()").extract_first()).strip()
        c_info["regis_address"] = str(response.xpath("//table[@class='addProjectTable siteFrome_info']/tr[3]/td[2]/text()").extract_first()).strip()
        c_info["social_credit_code"] = str(response.xpath("//table[@class='addProjectTable siteFrome_info']/tr[4]/td[2]/text()").extract_first()).strip()
        c_info["regis_type"] = str(response.xpath("//table[@class='addProjectTable siteFrome_info']/tr[5]/td[2]/text()").extract_first()).strip()
        c_info["registered_capital"] = str(response.xpath("//table[@class='addProjectTable siteFrome_info']/tr[6]/td[2]/text()").extract_first()).strip("\r\n\t人民币").replace(",","")
        c_info["url"] = response.url
        c_info["source"] = "江西"
        yield c_info
        c_apt = CompanyaptitudeItem()
        c_apt["province_company_id"] = c_info["province_company_id"]
        c_apt["company_name"] = c_info["company_name"]
        c_apt["aptitude_id"] = str(response.xpath("//table[@class='addProjectTable siteFrome_info']/tr[7]/td[2]/text()").extract_first()).strip()
        c_apt["aptitude_endtime"] = str(response.xpath("//table[@class='addProjectTable siteFrome_info']/tr[8]/td[2]/text()").extract_first()).strip()
        c_apt["aptitude_organ"] = str(response.xpath("//table[@class='addProjectTable siteFrome_info']/tr[9]/td[2]/text()").extract_first()).strip()
        c_apt["source"] = "江西"
        tr_list=response.xpath("//table[@class='listTable hoverTable trbgTable detailPopupTable']/tbody/tr")
        if tr_list:
            for tr in tr_list:
                c_apt["level"] = tr.xpath("./td[2]/text()").extract_first()
                c_apt["aptitude_name"] = tr.xpath("./td[3]/text()").extract_first()
                c_apt["check_time"] = tr.xpath("./td[4]/text()").extract_first()
                yield c_apt

