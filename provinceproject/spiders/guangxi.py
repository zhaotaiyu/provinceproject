# -*- coding: utf-8 -*-
import datetime
import json

import scrapy
from scrapy import FormRequest,Request
from provinceproject.items import *
class GuangxiSpider(scrapy.Spider):
    name = 'guangxi'
    custom_settings = {
        'DOWNLOAD_DELAY' : '1',
        #'DOWNLOADER_MIDDLEWARES' : {'provinceproject.middlewares.AbuyunProxyMiddleware': 543}
    }
    #allowed_domains = ['dn4.gxzjt.gov.cn:1141/WebInfo/Enterprise/Enterprise.aspx']
    start_urls = ['http://dn4.gxzjt.gov.cn:1141/WebInfo/Enterprise/Enterprise.aspx']

    def parse(self, response):
        url="http://dn4.gxzjt.gov.cn:1141/WebInfo/Enterprise/Enterprise.aspx"
        total_page=response.xpath("//div[@id='ContentPlaceHolder1_List_Pager']/table/tr/td/text()").extract_first()
        print(response.request.headers)
        print(type(response.request.headers.__repr__()))
        print(response.headers)

        if total_page:
            total_page=total_page.split("页")[0].split("/")[-1]
            __VIEWSTATE=response.xpath("//input[@id='__VIEWSTATE']/@value").extract_first()
            __VIEWSTATEGENERATOR=response.xpath("//input[@id='__VIEWSTATEGENERATOR']/@value").extract_first()
            __EVENTVALIDATION=response.xpath("//input[@id='__EVENTVALIDATION']/@value").extract_first()
            __CSRFTOKEN=response.xpath("//input[@id='__CSRFTOKEN']/@value").extract_first()
            __EVENTTARGET=response.xpath("//input[@id='__EVENTTARGET']/@value").extract_first()
            #for page in range(1,int(total_page)+1):
            # for page in range(1, 2):
            #     formdata={
            #         '__CSRFTOKEN': __CSRFTOKEN,
            #         '__VIEWSTATE': __VIEWSTATE,
            #         '__VIEWSTATEGENERATOR': __VIEWSTATEGENERATOR,
            #         '__EVENTTARGET': 'ctl00$ctl00$ContentPlaceHolder1$List$Pager',
            #         '__EVENTARGUMENT': str(page),
            #         '__EVENTVALIDATION': __EVENTVALIDATION,
            #         'ctl00$ctl00$ContentPlaceHolder1$Search$DanWeiName': '',
            #         'ctl00$ctl00$ContentPlaceHolder1$Search$DanWeiType': '',
            #         'ctl00$ctl00$ContentPlaceHolder1$Search$ZiZhiNum': '',
            #         'ctl00$ctl00$ContentPlaceHolder1$Search$CityNum': '',
            #         'ctl00$ctl00$ContentPlaceHolder1$Search$ZiZhiEndDate': ''
            #     }
            #     yield FormRequest(url,formdata=formdata,callback=self.parse_company_list)

    def parse_company_list(self,response):
        tr_list=response.xpath("//table[@id='ContentPlaceHolder1_List_Datagrid1']/tr")
        if tr_list:
            for tr in tr_list[1:]:
                company_url=tr.xpath("./td[2]/a/@href").extract_first()
                if company_url:
                    company_url="http://dn4.gxzjt.gov.cn:1141/WebInfo/Enterprise/"+company_url
                    yield Request(company_url,callback=self.parse_company)

    def parse_company(self,response):
        guangxi=GuangxiItem()
        guangxi["id"] =response.url.split("=")[-1]
        guangxi["name"] =response.xpath("//table[@id='ContentPlaceHolder1_tbcontent']/tr[1]/td[2]/span/text()").extract_first()
        guangxi["leal_person"] =response.xpath("//table[@id='ContentPlaceHolder1_tbcontent']/tr[3]/td[2]/span/text()").extract_first()
        guangxi["build_date"] =response.xpath("//table[@id='ContentPlaceHolder1_tbcontent']/tr[4]/td[2]/span/text()").extract_first()
        guangxi["contact_person"] =response.xpath("//table[@id='ContentPlaceHolder1_tbcontent']/tr[5]/td[2]/span/text()").extract_first()
        guangxi["lic_num"] =response.xpath("//table[@id='ContentPlaceHolder1_tbcontent']/tr[6]/td[2]/span/text()").extract_first()
        guangxi["reg_address"] =response.xpath("//table[@id='ContentPlaceHolder1_tbcontent']/tr[7]/td[2]/span/text()").extract_first()
        guangxi["remark"] =response.xpath("//table[@id='ContentPlaceHolder1_tbcontent']/tr[8]/td[2]/text()").extract_first().strip()
        guangxi["registered_capital"] =response.xpath("//table[@id='ContentPlaceHolder1_tbcontent']/tr[2]/td[4]/span/text()").extract_first()
        guangxi["leal_person_title"] =response.xpath("//table[@id='ContentPlaceHolder1_tbcontent']/tr[3]/td[4]/span/text()").extract_first()
        guangxi["postalcode"] =response.xpath("//table[@id='ContentPlaceHolder1_tbcontent']/tr[4]/td[4]/span/text()").extract_first()
        guangxi["contact_phone"] =response.xpath("//table[@id='ContentPlaceHolder1_tbcontent']/tr[5]/td[4]/text()").extract_first().strip()
        guangxi["contact_address"] =response.xpath("//table[@id='ContentPlaceHolder1_tbcontent']/tr[7]/td[4]/span/text()").extract_first()
        guangxi["social_credit_code"] =response.xpath("//table[@id='ContentPlaceHolder1_tbcontent']/tr[2]/td[6]/span/text()").extract_first()
        guangxi["tech_lead_duty"] =response.xpath("//table[@id='ContentPlaceHolder1_tbcontent']/tr[3]/td[6]/span/text()").extract_first()
        guangxi["fax"] =response.xpath("//table[@id='ContentPlaceHolder1_tbcontent']/tr[5]/td[6]/text()").extract_first().strip()
        guangxi["url"] =response.url
        guangxi["create_time"] =datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        guangxi["modification_time"] =datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        guangxi["is_delete"] =0
        div_list=response.xpath("//div[@id='ContentPlaceHolder1_UpdatePanel1']/fieldset/div")
        if div_list:
            for div in div_list:
                guangxi["aptitude_num"] =div.xpath("./table/tbody/tr[2]/td[1]/text()").extract_first()
                guangxi["aptitude_organ"] =div.xpath("./table/tbody/tr[2]/td[2]/text()").extract_first()
                guangxi["aptitude_accept_date"] =div.xpath("./table/tbody/tr[2]/td[3]/text()").extract_first()
                guangxi["aptitude_useful_date"] =div.xpath("./table/tbody/tr[2]/td[4]/text()").extract_first()
                guangxi["aptitude_type"] =div.xpath("./table/tbody/tr[2]/td[5]/text()").extract_first()
                guangxi["aptitude_range"] =div.xpath("./table/tbody/tr[3]/td[2]/text()").extract_first()
                yield guangxi



