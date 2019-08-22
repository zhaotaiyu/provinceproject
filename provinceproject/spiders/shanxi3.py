# -*- coding: utf-8 -*-
import datetime
import scrapy
from scrapy import FormRequest, Request
from provinceproject.items import *

#陕西
class Shanxi3Spider(scrapy.Spider):
    name = 'shanxi3'
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
        shanxi3=Shanxi3Item()
        shanxi3["id"] =response.url.split("=")[-1]
        shanxi3["name"] =response.xpath("//table[@class='m_table']/tr[1]/td[2]/span/text()").extract_first()
        shanxi3["lic_accept_date"] =response.xpath("//table[@class='m_table']/tr[2]/td[2]/span/text()").extract_first()
        shanxi3["aptitude_type"] =response.xpath("//table[@class='m_table']/tr[3]/td[2]/span/text()").extract_first()
        shanxi3["social_credit_code"] =response.xpath("//table[@class='m_table']/tr[4]/td[2]/span/text()").extract_first()
        shanxi3["reg_address"] =response.xpath("//table[@class='m_table']/tr[5]/td[2]/span/text()").extract_first()
        shanxi3["lic_num"] =response.xpath("//table[@class='m_table']/tr[1]/td[4]/span/text()").extract_first()
        shanxi3["lic_useful_date"] =response.xpath("//table[@class='m_table']/tr[2]/td[4]/span/text()").extract_first()
        shanxi3["leal_person"] =response.xpath("//table[@class='m_table']/tr[4]/td[4]/span/text()").extract_first()
        shanxi3["url"] =response.url
        shanxi3["create_time"] =datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        shanxi3["modification_time"] =datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        shanxi3["is_delete"] =0
        yield shanxi3



