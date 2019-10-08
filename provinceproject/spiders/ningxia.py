# -*- coding: utf-8 -*-
import json

import datetime
import scrapy
from scrapy import FormRequest,Request
from provinceproject.items import *
class NingxiaSpider(scrapy.Spider):
    name = 'ningxia'
    custom_settings = {
        'DOWNLOAD_DELAY': '0.1',
        # 'DOWNLOADER_MIDDLEWARES': {'provinceproject.middlewares.AbuyunProxyMiddleware': 543, }
    }
    #allowed_domains = ['www.nxjscx.com.cn/qysj.htm#']
    start_urls = ['http://www.nxjscx.com.cn/qysj.htm#/']
    def start_requests(self):
        url = "http://218.95.173.11:8092/portal.php?"
        p_list=[1,2,3,4,5,6,7,10,11,12]
        #p_list = [1]
        for ci_qualification_code in p_list:
            formdata={
                'page': '1',
                'resid': 'web_company.quaryCorp',
                'ci_qualification_code': str(ci_qualification_code),
                'ci_islocal_code': 'JN01',
                'rows': '15'
            }
            yield FormRequest(url,callback=self.parse,formdata=formdata,meta={'ci_qualification_code':ci_qualification_code,'page':'1'})
            beianformdata = {
                'page': '1',
                'resid': 'web_company.quaryCorp',
                'ci_qualification_code': str(ci_qualification_code),
                'ci_islocal_code': 'JN02',
                'rows': '15'
            }
            yield FormRequest(url, callback=self.parse_beian, formdata=beianformdata,meta={'ci_qualification_code':ci_qualification_code,'page':'1'})

    def parse(self, response):
        data=json.loads(response.text).get("data")
        if data:
            for info in data:
                rowid=info.get("id")
                corp_id=info.get("corp_id")
                company_url="http://218.95.173.11:8092/selectact/query.jspx?resid=IDIXWP2KBO&rowid={}&rows=10".format(rowid)
                yield Request(company_url,callback=self.parse_company,meta={"corp_id":corp_id})
        if len(data)==15:
            request = self.next_page(response.meta.get("page"),response.meta.get("ci_qualification_code"),response.url,back=self.parse,ci_islocal_code='JN01')
            yield request
    def next_page(self,page,ci_qualification_code,url,back,ci_islocal_code):
        page = str(int(page)+1)
        formdata = {
            'page': page,
            'resid': 'web_company.quaryCorp',
            'ci_qualification_code': str(ci_qualification_code),
            'ci_islocal_code': ci_islocal_code,
            'rows': '15'
        }
        return FormRequest(url, callback=back, formdata=formdata,meta={'ci_qualification_code': ci_qualification_code, 'page': page})

    def parse_company(self,response):
        data_list = json.loads(response.text).get("data")
        for data in data_list:
            c_info = CompanyInfomortation()
            c_info["province_company_id"] = "ningxia_" + data.get("corp_id")
            c_info["company_name"] = data.get("ci_name")
            c_info["regis_address"] = data.get("ci_reg_addr")
            c_info["social_credit_code"] = data.get("ci_code")
            c_info["registered_capital"] = data.get("ci_reg_capital")
            c_info["leal_person"] = data.get("ci_legal_person")
            c_info["build_date"] = data.get("ci_establish_date")
            c_info["tel"] = data.get("ci_phone")
            c_info["fax"] = data.get("ci_fax")
            c_info["website"] = data.get("ci_website")
            c_info["email"] = data.get("ci_email")
            c_info["postalcode"] = data.get("ci_postcode")
            c_info["area_code"] = str(data.get("ci_province")) + str(data.get("ci_city")) + str(data.get("ci_county"))
            c_info["contact_person"] = data.get("ci_link_man")
            c_info["tel"] = data.get("ci_link_phone")
            c_info["contact_phone"] = data.get("ci_link_mobile")
            c_info["source"] = "宁夏"
            yield c_info
            aptitude_url = "http://218.95.173.11:8092/selectact/query.jspx?resid=IDIXWTKRCN&corp_id={}&rows=30".format(response.meta.get("corp_id"))
            yield Request(aptitude_url,callback=self.parse_aptitude,meta={"company_name":c_info["company_name"],"province_company_id":c_info["province_company_id"]})
    def parse_aptitude(self,response):
        data_list = json.loads(response.text).get("data")
        ningxia=response.meta.get("ningxia")
        for data in data_list:
            c_apt = CompanyaptitudeItem()
            c_apt["province_company_id"] = response.meta.get("province_company_id")
            c_apt["company_name"] = response.meta.get("company_name")
            c_apt["aptitude_large"]=data.get("cqs_sequence")
            c_apt["aptitude_major"]=data.get("cqs_speciality")
            c_apt["aptitude_type"]=data.get("cq_type")
            c_apt["level"]=data.get("cqs_level")
            c_apt["source"] = "宁夏"
            yield c_apt
    def parse_beian(self,response):
        data = json.loads(response.text).get("data")
        if data:
            for info in data:
                beian=BeianItem()
                beian["social_credit_code"] = info.get("ci_code")
                beian["company_name"] = info.get("ci_name")
                beian["record_province"] = "宁夏"
                yield beian
        if len(data)==15:
            request = self.next_page(response.meta.get("page"),response.meta.get("ci_qualification_code"),response.url,back=self.parse_beian,ci_islocal_code='JN02')
            yield request



