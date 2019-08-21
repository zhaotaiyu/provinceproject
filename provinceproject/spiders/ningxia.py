# -*- coding: utf-8 -*-
import json

import datetime
import scrapy
from scrapy import FormRequest,Request
from provinceproject.items import *

class NingxiaSpider(scrapy.Spider):
    name = 'ningxia'
    #allowed_domains = ['www.nxjscx.com.cn/qysj.htm#']
    start_urls = ['http://www.nxjscx.com.cn/qysj.htm#/']
    def start_requests(self):
        url = "http://218.95.173.11:8092/portal.php?"
        list=[1,2,3,4,5,6,7,10,11,12]
        for ci_qualification_code in list:
            formdata={
                'page': '1',
                'resid': 'web_company.quaryCorp',
                'ci_qualification_code': str(ci_qualification_code),
                'ci_islocal_code': 'JN01',
                'rows': '99999'
            }
            yield FormRequest(url,callback=self.parse,formdata=formdata)
            beianformdata = {
                'page': '1',
                'resid': 'web_company.quaryCorp',
                'ci_qualification_code': str(ci_qualification_code),
                'ci_islocal_code': 'JN02',
                'rows': '99999'
            }
            yield FormRequest(url, callback=self.parse_beian, formdata=beianformdata)

    def parse(self, response):
        data=json.loads(response.text).get("data")
        if data:
            for info in data:
                rowid=info.get("id")
                corp_id=info.get("corp_id")
                company_url="http://218.95.173.11:8092/selectact/query.jspx?resid=IDIXWP2KBO&rowid={}&rows=10".format(rowid)
                yield Request(company_url,callback=self.parse_company,meta={"corp_id":corp_id})

    def parse_company(self,response):
        data_list = json.loads(response.text).get("data")
        for data in data_list:
            ningxia=NingxiaItem()
            ningxia["id"] = data.get("corp_id")
            ningxia["name"] = data.get("ci_name")
            ningxia["reg_address"] = data.get("ci_reg_addr")
            ningxia["social_credit_code"] = data.get("ci_code")
            ningxia["registered_capital"] = data.get("ci_reg_capital")
            ningxia["leal_person"] = data.get("ci_legal_person")
            ningxia["build_date"] = data.get("ci_establish_date")
            ningxia["tel"] = data.get("ci_phone")
            ningxia["fax"] = data.get("ci_fax")
            ningxia["website"] = data.get("ci_website")
            ningxia["email"] = data.get("ci_email")
            ningxia["postalcode"] = data.get("ci_postcode")
            ningxia["reg_address_province"] = data.get("ci_province")
            ningxia["reg_address_city"] = data.get("ci_city")
            ningxia["reg_address_country"] = data.get("ci_county")
            ningxia["contact_person"] = data.get("ci_link_man")
            ningxia["contact_tel"] = data.get("ci_link_phone")
            ningxia["contact_phone"] = data.get("ci_link_mobile")
            ningxia["create_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ningxia["modification_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ningxia["is_delete"] = 0
            aptitude_url = "http://218.95.173.11:8092/selectact/query.jspx?resid=IDIXWTKRCN&corp_id={}&rows=30".format(response.meta.get("corp_id"))
            yield Request(aptitude_url,callback=self.parse_aptitude,meta={"ningxia":ningxia})
    def parse_aptitude(self,response):
        data_list = json.loads(response.text).get("data")
        ningxia=response.meta.get("ningxia")
        for data in data_list:
            ningxia["aptitude_credit_score"]=data.get("cq_credit_score")
            ningxia["aptitude_sequence"]=data.get("cqs_sequence")
            ningxia["aptitude_credit_level"]=data.get("cq_credit_level")
            ningxia["aptitude_speciality"]=data.get("cqs_speciality")
            ningxia["aptitude_type"]=data.get("cq_type")
            ningxia["aptitude_level"]=data.get("cqs_level")
            yield ningxia
    def parse_beian(self,response):
        data = json.loads(response.text).get("data")
        if data:
            for info in data:
                beian=BeianItem()
                beian["corpcode"] = info.get("ci_code")
                beian["corpname"] = info.get("ci_name")
                beian["danweitype"] = info.get("ci_qualification")
                beian["legalman"] = info.get("ci_legal")
                beian["address"] = info.get("ci_reg_addr")
                beian["record_province"] = "宁夏"
                beian["create_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                beian["modification_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                beian["is_delete"] = 0
                yield beian



