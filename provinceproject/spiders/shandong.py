# -*- coding: utf-8 -*-
import json

import datetime
import scrapy
from scrapy import Request
from provinceproject.items import *


class ShandongSpider(scrapy.Spider):
    name = 'shandong'
    #allowed_domains = ['zjt.shandong.gov.cn']
    start_urls = ['http://zjt.shandong.gov.cn/']
    def start_requests(self):
        url="http://221.214.94.41:81/InformationReleasing/Ashx/InformationReleasing.ashx?methodname=GetCorpInfo&CorpName=&CorpCode=&CertType=112&LegalMan=&CurrPageIndex={}&PageSize=12&_=1565141169809"
        for page in range(1,1758):
            page_url=url.format(str(page))
            yield Request(page_url,callback=self.parse)
        #备案
        beian_url="http://221.214.94.41:81/InformationReleasing/Ashx/InformationReleasing.ashx?methodname=getoutprovincecorpinfo&CorpName=&CorpCode=&DanWeiType=&CurrPageIndex=1&PageSize=10043&_=1565146277905"
        #yield Request(beian_url,callback=self.parse_beian)
    def parse(self, response):
        corpinfo_list=json.loads(response.text).get("data").get("CorpInfoList")
        if corpinfo_list:
            for corp in corpinfo_list:
                CorpCode=corp.get("CorpCode")
                CorpNamefdc=corp.get("CorpName")
                company_url="http://221.214.94.41:81/InformationReleasing/Ashx/InformationReleasing.ashx?methodname=GetCorpQualificationCertInfo&CorpCode={}&CorpNamefdc={}&CurrPageIndex=1&PageSize=5&_=1565145293507".format(CorpCode,CorpNamefdc)
                yield Request(company_url,callback=self.parse_company)
    def parse_company(self,response):
        shandong=ShandongItem()
        corpqualificationcertlist = json.loads(response.text).get("data").get("CorpQualificationCertList")
        if corpqualificationcertlist:
            for company in corpqualificationcertlist:
                shandong["show"] =company.get("Show")
                shandong["timestamp"] =company.get("TimeStamp")
                shandong["certid"] =company.get("CertID")
                shandong["organname"] =company.get("OrganName")
                shandong["organdate"] =company.get("OrganDate")
                shandong["ceoname"] =company.get("CEOName")
                shandong["ctoname"] =company.get("CTOName")
                shandong["enddate"] =company.get("EndDate")
                shandong["qualificationscope"] =company.get("QualificationScope")
                shandong["corpcode"] =company.get("CorpCode")
                shandong["corpname"] =company.get("CorpName")
                shandong["sourceouname"] =company.get("SourceOuName")
                shandong["create_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                shandong["modification_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                shandong["is_delete"] = 0
                yield shandong

    def parse_beian(self,response):
        corpinfolist = json.loads(response.text).get("data").get("CorpInfoList")
        if corpinfolist:
            for company in corpinfolist:
                beian=BeianItem()
                beian["corpcode"] = company.get("CorpCode")
                beian["corpname"] = company.get("CorpName")
                beian["danweitype"] = company.get("DanWeiType")
                beian["areacode"] = company.get("AreaCode")
                beian["areaname"] = company.get("AreaName")
                beian["certcode"] = company.get("CertCode")
                beian["validdate"] = company.get("ValidDate")
                beian["qualificationscope"] = company.get("QualificationScope")
                beian["regprin"] = company.get("RegPrin").strip("万人民币")
                beian["legalman"] = company.get("LegalMan")
                beian["legalmanprotitle"] = company.get("LegalManProTitle")
                beian["legalmanduty"] = company.get("LegalManDuty")
                beian["economicnum"] = company.get("EconomicNum")
                beian["corpbirthdate"] = company.get("CorpBirthDate")
                beian["postalcode"] = company.get("PostalCode")
                beian["linkman"] = company.get("LinkMan")
                beian["linktel"] = company.get("LinkTel")
                beian["fax"] = company.get("Fax")
                beian["address"] = company.get("Address")
                beian["titlelevelnum"] = company.get("TitleLevelNum")
                beian["record_province"] = "山东"
                beian["create_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                beian["modification_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                beian["is_delete"] = 0
                yield beian



































