# -*- coding: utf-8 -*-
import datetime
import scrapy
from scrapy import FormRequest,Request
from provinceproject.items import *

class HubeiSpider(scrapy.Spider):
    name = 'hubei'
    #allowed_domains = ['59.175.169.110/ewmwz/qymanage/qyzzsearch.aspx?ssl=109']
    start_urls = ['http://jg.hbcic.net.cn/web/QyManage/QyList.aspx']
    def parse(self, response):
        total_page = response.xpath("//span[@id='labPageCount']/text()").extract_first()
        __VIEWSTATE=response.xpath("//input[@id='__VIEWSTATE']/@value").extract_first()
        __EVENTVALIDATION=response.xpath("//input[@id='__EVENTVALIDATION']/@value").extract_first()
        for page in range(1,int(total_page)+1):
            formdata={
                '__EVENTTARGET': 'lbtnGo',
                '__EVENTVALIDATION': __EVENTVALIDATION,
                '__VIEWSTATE':__VIEWSTATE,
                'txtPageIndex': str(page),
            }
            yield scrapy.FormRequest(url=response.url,formdata=formdata,callback=self.parse_companylist)
    def parse_companylist(self,response):
        tr_list=response.xpath("//table[@class='table']/tr")
        for tr in tr_list[1:-1]:
            company_url=tr.xpath("./td[2]/a/@href").extract_first()
            if company_url:
                company_url="http://jg.hbcic.net.cn/web/QyManage/"+company_url
                yield Request(company_url,callback=self.parse_company)
    def parse_company(self,response):
        hubei=HubeiItem()
        hubei["id"] = response.url.split("=")[-1]
        hubei["name"] = str(response.xpath("//form[@id='form1']/table/tr/td/table/tr[7]/td/table/tr[2]/td[2]/text()").extract_first()).strip()
        hubei["reg_address"] = str(response.xpath("//form[@id='form1']/table/tr/td/table/tr[7]/td/table/tr[3]/td[2]/text()").extract_first()).strip()
        hubei["social_credit_code"] = str(response.xpath("//form[@id='form1']/table/tr/td/table/tr[7]/td/table/tr[4]/td[2]/text()").extract_first()).strip()
        hubei["regis_type"] = str(response.xpath("//form[@id='form1']/table/tr/td/table/tr[7]/td/table/tr[5]/td[2]/text()").extract_first()).strip()
        hubei["leal_person"] = str(response.xpath("//form[@id='form1']/table/tr/td/table/tr[7]/td/table/tr[6]/td[2]/text()").extract_first()).strip()
        hubei["leal_person_duty"] = str(response.xpath("//form[@id='form1']/table/tr/td/table/tr[7]/td/table/tr[7]/td[2]/text()").extract_first()).strip()
        hubei["tech_lead"] = str(response.xpath("//form[@id='form1']/table/tr/td/table/tr[7]/td/table/tr[9]/td[2]/text()").extract_first()).strip()
        hubei["tech_lead_duty"] = str(response.xpath("//form[@id='form1']/table/tr/td/table/tr[7]/td/table/tr[10]/td[2]/text()").extract_first()).strip()
        hubei["anistrative_lic_num"] = str(response.xpath("//form[@id='form1']/table/tr/td/table/tr[7]/td/table/tr[11]/td[2]/text()").extract_first()).strip()
        hubei["lic_start_date"] = str(response.xpath("//form[@id='form1']/table/tr/td/table/tr[7]/td/table/tr[12]/td[2]/text()").extract_first()).strip()
        hubei["lic_organ"] = str(response.xpath("//form[@id='form1']/table/tr/td/table/tr[7]/td/table/tr[13]/td[2]/text()").extract_first()).strip()
        hubei["remark"] = str(response.xpath("//form[@id='form1']/table/tr/td/table/tr[7]/td/table/tr[14]/td[2]/text()").extract_first()).strip()
        hubei["registered_capital"] = str(response.xpath("//form[@id='form1']/table/tr/td/table/tr[7]/td/table/tr[5]/td[4]/text()").extract_first()).strip()
        hubei["build_date"] = str(response.xpath("//form[@id='form1']/table/tr/td/table/tr[7]/td/table/tr[6]/td[4]/text()").extract_first()).strip()
        hubei["leal_person_title"] = str(response.xpath("//form[@id='form1']/table/tr/td/table/tr[7]/td/table/tr[9]/td[4]/text()").extract_first()).strip()
        hubei["technicalleader_title"] = str(response.xpath("//form[@id='form1']/table/tr/td/table/tr[7]/td/table/tr[10]/td[4]/text()").extract_first()).strip()
        hubei["lic_num"] = str(response.xpath("//form[@id='form1']/table/tr/td/table/tr[7]/td/table/tr[11]/td[4]/text()").extract_first()).strip()
        hubei["lic_useful_date"] = str(response.xpath("//form[@id='form1']/table/tr/td/table/tr[7]/td/table/tr[12]/td[4]/text()").extract_first()).strip()
        hubei["lic_indate"] = str(response.xpath("//form[@id='form1']/table/tr/td/table/tr[7]/td/table/tr[13]/td[4]/text()").extract_first()).strip()
        hubei["lic_name"] = str(response.xpath("//form[@id='form1']/table/tr/td/table/tr[9]/td/table/tr[2]/td[1]/text()").extract_first()).strip()
        if hubei["lic_start_date"]=='None':
            hubei["lic_start_date"]=str(response.xpath("//form[@id='form1']/table/tr/td/table/tr[9]/td/table/tr[2]/td[2]/text()").extract_first()).strip()
        hubei["url"] = response.url
        hubei["create_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        hubei["modification_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        hubei["is_delete"] = 0
        yield hubei