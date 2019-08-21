# -*- coding: utf-8 -*-
import json
import datetime
from lxml import etree
from provinceproject.items import *
from scrapy import FormRequest,Request
class NeimengguSpider(scrapy.Spider):
    name = 'neimenggu'
    #allowed_domains = ['110.16.70.26/nmjgpublisher/corpinfo/CorpInfoObtain.aspx']
    start_urls = ['http://110.16.70.26/nmjgpublisher/corpinfo/CorpInfoObtain.aspx/']
    def parse(self, response):
        for page in range(1,39):
            url="http://110.16.70.26/nmjgpublisher/handle/ProjectsInfoHandler.ashx?type=CorpInfo&lblPageCount=38&lblPageIndex={}&lblRowsCount=757&lblPageSize=20&SFZBDL=&CorpName=&Zzlx=&CertNum=&City=&_=1565252583301".format(str(page))
            #yield Request(url,callback=self.parse_conmanylist)
        #备案
        beian_url="http://110.16.70.26/nmjgpublisher/handle/ProjectsInfoHandler.ashx?type=CorpInfoQW&SFZBDL=&CorpName=&Zzlx=&CertNum=&City=&nPageIndex=1&nPageCount=0&nPageRowsCount=0&nPageSize=20"
        yield Request(beian_url,callback=self.parse_beiancompanylist)
    def parse_conmanylist(self,response):
        tb=json.loads(response.text).get("tb")
        tree=etree.HTML(tb)
        tr_list=tree.xpath("//tr")
        if tr_list:
            for tr in tr_list:
                company_url=tr.xpath("./td[2]/a/@onclick")[0]
                CorpCode=company_url.split("'")[1]
                CorpName=company_url.split("'")[3]
                company_url="http://110.16.70.26/nmjgpublisher/corpinfo/CorpDetailInfoObtain.aspx?CorpCode={}&CorpName={}&VType=1".format(CorpCode,CorpName)
                yield Request(company_url,callback=self.parse_company,meta={"CorpCode":CorpCode,"CorpName":CorpName})
    def parse_company(self,response):
        neimenggu=NeimengguItem()
        neimenggu["id"] =response.meta.get("CorpCode")
        neimenggu["name"] =response.meta.get("CorpName")
        neimenggu["social_credit_code"] =response.meta.get("CorpCode")
        neimenggu["leal_person"] =str(response.xpath("//div[@class='basic_infor']/table/tr[3]/td[2]/text()").extract_first()).strip()
        neimenggu["regis_type"] =str(response.xpath("//div[@class='basic_infor']/table/tr[4]/td[2]/text()").extract_first()).strip()
        neimenggu["contact_person"] =str(response.xpath("//div[@class='basic_infor']/table/tr[5]/td[2]/text()").extract_first()).strip()
        neimenggu["contact_address"] =str(response.xpath("//div[@class='basic_infor']/table/tr[6]/td[2]/text()").extract_first()).strip()
        try:
            neimenggu["registered_capital"] =str(response.xpath("//div[@class='basic_infor']/table/tr[2]/td[4]/text()").extract_first()).strip().strip("万元(人民币)")
        except:
            neimenggu["registered_capital"] = str(
                response.xpath("//div[@class='basic_infor']/table/tr[2]/td[4]/text()").extract_first()).strip()
        neimenggu["leal_person_title"] =str(response.xpath("//div[@class='basic_infor']/table/tr[3]/td[4]/text()").extract_first()).strip()
        neimenggu["build_date"] =str(response.xpath("//div[@class='basic_infor']/table/tr[4]/td[4]/text()").extract_first()).strip()
        neimenggu["reg_address"] =str(response.xpath("//div[@class='basic_infor']/table/tr[5]/td[4]/text()").extract_first()).strip()
        neimenggu["tech_lead_duty"] =str(response.xpath("//div[@class='basic_infor']/table/tr[3]/td[6]/text()").extract_first()).strip()
        neimenggu["postalcode"] =str(response.xpath("//div[@class='basic_infor']/table/tr[4]/td[6]/text()").extract_first()).strip()
        neimenggu["reg_address_city"] =str(response.xpath("//div[@class='basic_infor']/table/tr[5]/td[6]/text()").extract_first()).strip()
        neimenggu["url"] =response.url
        neimenggu["create_time"] =datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        neimenggu["modification_time"] =datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        neimenggu["is_delete"] =0
        table_list=response.xpath("//table[@class='no_list_table']")
        if table_list:
            for table in table_list:
                neimenggu["aptitude_num"] =str(table.xpath("./tr[1]/td[2]/text()").extract_first()).strip()
                neimenggu["aptitude_accept_date"] =str(table.xpath("./tr[2]/td[2]/text()").extract_first()).strip()
                neimenggu["aptitude_range"] =str(table.xpath("./tr[3]/td[2]/text()").extract_first()).strip()
                neimenggu["aptitude_organ"] =str(table.xpath("./tr[1]/td[4]/text()").extract_first()).strip()
                neimenggu["aptitude_useful_date"] =str(table.xpath("./tr[2]/td[4]/text()").extract_first()).strip()
                neimenggu["com_lead"] =str(table.xpath("./tr[1]/td[6]/text()").extract_first()).strip()
                neimenggu["tech_lead"] =str(table.xpath("./tr[2]/td[6]/text()").extract_first()).strip()
                yield neimenggu
        else:
            yield neimenggu

    def parse_beiancompanylist(self,response):
        tb = json.loads(response.text).get("tb")
        tree = etree.HTML(tb)
        tr_list = tree.xpath("//tr")
        if tr_list:
            for tr in tr_list:
                company_url = tr.xpath("./td[2]/a/@onclick")[0]
                CorpCode = company_url.split("'")[1]
                CorpName = company_url.split("'")[3]
                RecordGuid= company_url.split("'")[5]
                company_url = "http://110.16.70.26/nmjgpublisher/corpinfo/CorpDetailInfoObtain.aspx?CorpCode={}&CorpName={}&VType=2&RecordGuid={}".format(CorpCode, CorpName,RecordGuid)
                yield Request(company_url, callback=self.parse_beiancompany, meta={"CorpCode": CorpCode, "CorpName": CorpName})
    def parse_beiancompany(self,response):
        beian = BeianItem()
        beian["corpcode"] = response.meta.get("CorpCode")
        beian["corpname"] =str(response.xpath("//table[@class='cpd_basic_table']/tr[1]/td[2]/text()").extract_first()).strip()
        beian["areaname"] =str(response.xpath("//table[@class='cpd_basic_table']/tr[5]/td[6]/text()").extract_first()).strip()
        beian["certcode"] = str(response.xpath("//table[@class='cpd_basic_table']/tr[2]/td[2]/text()").extract_first()).strip()
        try:
            beian["regprin"] = str(response.xpath("//table[@class='cpd_basic_table']/tr[2]/td[4]/text()").extract_first()).strip().strip("万元(人民币)")
        except:
            beian["regprin"] = str(response.xpath("//table[@class='cpd_basic_table']/tr[2]/td[4]/text()").extract_first()).strip()
        beian["legalman"] = str(response.xpath("//table[@class='cpd_basic_table']/tr[3]/td[2]/text()").extract_first()).strip()
        beian["legalmanprotitle"] = str(response.xpath("//table[@class='cpd_basic_table']/tr[3]/td[4]/text()").extract_first()).strip()
        beian["legalmanduty"] = str(response.xpath("//table[@class='cpd_basic_table']/tr[3]/td[6]/text()").extract_first()).strip()
        beian["economicnum"] = str(response.xpath("//table[@class='cpd_basic_table']/tr[4]/td[2]/text()").extract_first()).strip()
        beian["corpbirthdate"] = str(response.xpath("//table[@class='cpd_basic_table']/tr[4]/td[4]/text()").extract_first()).strip()
        beian["postalcode"] = str(response.xpath("//table[@class='cpd_basic_table']/tr[4]/td[6]/text()").extract_first()).strip()
        beian["linkman"] = str(response.xpath("//table[@class='cpd_basic_table']/tr[5]/td[2]/text()").extract_first()).strip()
        beian["address"] = str(response.xpath("//table[@class='cpd_basic_table']/tr[6]/td[2]/text()").extract_first()).strip()
        beian["record_province"] = "内蒙古"
        beian["create_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        beian["modification_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        beian["is_delete"] = 0
        yield beian



