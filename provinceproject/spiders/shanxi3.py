# -*- coding: utf-8 -*-
import datetime
import scrapy
from scrapy import FormRequest, Request
from provinceproject.items import *

#陕西
class Shanxi3Spider(scrapy.Spider):
    name = 'shanxi3'
    custom_settings = {
        'DOWNLOAD_DELAY': '0.1',
        # 'DOWNLOADER_MIDDLEWARES': {'provinceproject.middlewares.AbuyunProxyMiddleware': 543, }
    }
    #allowed_domains = ['www.shaanxijs.gov.cn:9010/SxApp/Share/Web/SgqyList.aspx']
    start_urls = ['http://www.shaanxijs.gov.cn:9010/SxApp/Share/Web/SgqyList.aspx/']
    def parse(self, response):
        url="http://www.shaanxijs.gov.cn:9010/SxApp/Share/Web/SgqyList.aspx"
        __VIEWSTATE=response.xpath("//input[@id='__VIEWSTATE']/@value").extract_first()
        __VIEWSTATEGENERATOR = response.xpath("//input[@id='__VIEWSTATEGENERATOR']/@value").extract_first()
        __EVENTVALIDATION = response.xpath("//input[@id='__EVENTVALIDATION']/@value").extract_first()
        total_page=response.xpath("//div[@id='Pager1']/table/tr/td[2]/b/text()").extract_first()
        if total_page:
            total_page=total_page.split("/")[-1].strip("页")
            for page in range (2,int(total_page)+1):
                formdata = {
                    '__VIEWSTATE': __VIEWSTATE,
                    '__VIEWSTATEGENERATOR': __VIEWSTATEGENERATOR,
                    '__EVENTTARGET': 'Pager1',
                    '__EVENTARGUMENT': str(page),
                    '__EVENTVALIDATION': __EVENTVALIDATION,
                    'Pager1_input': '1'
                }
                yield FormRequest(url,formdata=formdata,callback=self.parse_companylist)

    def parse_companylist(self,response):
        tr_list=response.xpath("//table[@class='m_dg1']/tr")
        if tr_list:
            for tr in tr_list[1:]:
                company_url=tr.xpath("./td[6]/a/@href").extract_first()
                if company_url:
                    company_url="http://www.shaanxijs.gov.cn:9010/SxApp/Share/Web/"+company_url
                    yield Request(company_url,callback=self.parse_company)
    def parse_company(self,response):
        c_info = CompanyInfomortation()
        c_info["province_company_id"] ="shanxi3_" + response.url.split("=")[-1]
        c_info["company_name"] =response.xpath("//table[@class='m_table']/tr[1]/td[2]/span/text()").extract_first()
        c_info["leal_person"] = response.xpath("//table[@class='m_table']/tr[4]/td[4]/span/text()").extract_first()
        c_info["social_credit_code"] = response.xpath("//table[@class='m_table']/tr[4]/td[2]/span/text()").extract_first()
        c_info["regis_address"] = response.xpath("//table[@class='m_table']/tr[5]/td[2]/span/text()").extract_first()
        c_info["url"] = response.url
        c_info["source"] = "陕西"
        yield c_info
        c_apt = CompanyaptitudeItem()
        c_apt["province_company_id"] = c_info["province_company_id"]
        c_apt["company_name"] = c_info["company_name"]
        c_apt["aptitude_startime"] =response.xpath("//table[@class='m_table']/tr[2]/td[2]/span/text()").extract_first()
        c_apt["aptitude_name"] =response.xpath("//table[@class='m_table']/tr[3]/td[2]/span/text()").extract_first()
        c_apt["aptitude_id"] =response.xpath("//table[@class='m_table']/tr[1]/td[4]/span/text()").extract_first()
        c_apt["aptitude_endtime"] =response.xpath("//table[@class='m_table']/tr[2]/td[4]/span/text()").extract_first()
        c_apt["source"] = "陕西"
        yield c_apt



