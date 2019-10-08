# -*- coding: utf-8 -*-
import json

import datetime
import scrapy
from scrapy import Request
from provinceproject.items import *


class ShandongSpider(scrapy.Spider):
    name = 'shandong'
    custom_settings = {
        'DOWNLOAD_DELAY': '0.3',
        #'DOWNLOADER_MIDDLEWARES': {'provinceproject.middlewares.AbuyunProxyMiddleware': 543, }
    }
    #allowed_domains = ['zjt.shandong.gov.cn']
    start_urls = ['http://zjt.shandong.gov.cn/']
    def start_requests(self):
        url="http://221.214.94.41:81/InformationReleasing/Ashx/InformationReleasing.ashx?methodname=GetCorpInfo&CorpName=&CorpCode=&CertType=112&LegalMan=&CurrPageIndex=1&PageSize=12&_=1565141169809"
        yield Request(url,callback=self.parse,meta={"page":1})
        #备案
        beian_url="http://221.214.94.41:81/InformationReleasing/Ashx/InformationReleasing.ashx?methodname=getoutprovincecorpinfo&CorpName=&CorpCode=&DanWeiType=&CurrPageIndex=1&PageSize=12&_=1569832413356"
        yield Request(beian_url,callback=self.parse_beian,meta={"page":1})
    def parse(self, response):
        if json.loads(response.text).get("status") =="成功":
            corpinfo_list=json.loads(response.text).get("data").get("CorpInfoList")
            if corpinfo_list:
                for corp in corpinfo_list:
                    CorpCode=corp.get("CorpCode")
                    CorpNamefdc=corp.get("CorpName")
                    company_url="http://221.214.94.41:81/InformationReleasing/Ashx/InformationReleasing.ashx?methodname=GetCorpQualificationCertInfo&CorpCode={}&CorpNamefdc={}&CurrPageIndex=1&PageSize=12&_=1565145293507".format(CorpCode,CorpNamefdc)
                    yield Request(company_url,callback=self.parse_company)
            total = json.loads(response.text).get("data").get("TotalNum")
            if int(response.meta.get("page"))*12<int(total):
                page = response.meta.get("page") + 1
                url = "http://221.214.94.41:81/InformationReleasing/Ashx/InformationReleasing.ashx?methodname=GetCorpInfo&CorpName=&CorpCode=&CertType=112&LegalMan=&CurrPageIndex={}&PageSize=12&_=1565141169809".format(page)
                yield Request(url,callback=self.parse,meta={"page":page})
        else:
            yield Request(response.url,callback=self.parse,dont_filter=True,meta={"page":response.meta.get("page"),})
    def parse_company(self,response):
        c_info=CompanyInfomortation()
        corpqualificationcertlist = json.loads(response.text).get("data").get("CorpQualificationCertList")
        if corpqualificationcertlist:
            for company in corpqualificationcertlist[1:2]:
                c_info["province_company_id"] = "shandong_" + company.get("CorpCode")
                c_info["social_credit_code"] = company.get("CorpCode")
                c_info["company_name"] = company.get("CorpName")
                c_info["source"] = "山东"
                c_info["ceoname"] = company.get("CEOName")
                c_info["ctoname"] = company.get("CTOName")
                yield c_info
            for company in corpqualificationcertlist:
                c_apt = CompanyaptitudeItem()
                c_apt["province_company_id"] = "shandong_" + company.get("CorpCode")
                c_apt["company_name"] = company.get("CorpName")
                c_apt["aptitude_id"] = company.get("CertID")
                c_apt["aptitude_organ"] = company.get("OrganName")
                c_apt["aptitude_startime"] =company.get("OrganDate")
                c_apt["aptitude_endtime"] = company.get("EndDate")
                c_apt["aptitude_name"] =company.get("QualificationScope")
                c_apt["source"] = "山东"
                yield c_apt
    def parse_beian(self,response):
        print(response.text)
        total = json.loads(response.text).get("data").get("TotalNum")
        status = json.loads(response.text).get("status")
        if status =="成功":
            corpinfolist = json.loads(response.text).get("data").get("CorpInfoList")
            if corpinfolist:
                for company in corpinfolist:
                    beian = BeianItem()
                    beian["social_credit_code"] = company.get("CorpCode")
                    beian["company_name"] = company.get("CorpName")
                    beian["record_province"] = "山东"
                    yield beian
            if int(response.meta.get("page"))*12<int(total):
                page = response.meta.get("page") + 1
                url = "http://221.214.94.41:81/InformationReleasing/Ashx/InformationReleasing.ashx?methodname=getoutprovincecorpinfo&CorpName=&CorpCode=&DanWeiType=&CurrPageIndex={}&PageSize=12&_=1569832413356".format(page)
                yield Request(url,callback=self.parse_beian,meta={"page":page+1})
        else:
            yield Request(response.url,callback=self.parse_beian,dont_filter=True)
    # def parse_beiandetail(self,response):
    #     status = json.loads(response.text).get("status")
    #     if status == "成功":
    #         corpinfolist = json.loads(response.text).get("data").get("CorpInfoList")
    #         if corpinfolist:
    #             for company in corpinfolist:
    #                 beian=BeianItem()
    #                 beian["corpcode"] = company.get("CorpCode")
    #                 beian["corpname"] = company.get("CorpName")
    #                 beian["record_province"] = "山东"
    #
    #                 yield beian
    #         else:
    #             yield Request(response.url, callback=self.parse_beiandetail, dont_filter=True)



































