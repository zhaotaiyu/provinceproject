# -*- coding: utf-8 -*-
import json
import datetime
from lxml import etree
from provinceproject.items import *
from scrapy import FormRequest,Request
class NeimengguSpider(scrapy.Spider):
    name = 'neimenggu'
    custom_settings = {
        'DOWNLOAD_DELAY': '0.1',
        'DOWNLOADER_MIDDLEWARES': {'provinceproject.middlewares.AbuyunProxyMiddleware': 543, }
    }
    #allowed_domains = ['110.16.70.26/nmjgpublisher/corpinfo/CorpInfoObtain.aspx']
    start_urls = ['http://110.16.70.26/nmjgpublisher/handle/ProjectsInfoHandler.ashx?type=CorpInfo&lblPageCount=0&lblPageIndex=1&lblRowsCount=0&lblPageSize=20&SFZBDL=&CorpName=&Zzlx=&CertNum=&City=&_=1570505601557','http://110.16.70.26/nmjgpublisher/handle/ProjectsInfoHandler.ashx?type=CorpInfoQW&SFZBDL=&CorpName=&Zzlx=&CertNum=&City=&nPageIndex=1&nPageCount=0&nPageRowsCount=0&nPageSize=20']
    def parse(self, response):
        total_page = int(json.loads(response.text).get("nPageCount"))+1
        for page in range(1,total_page):
            url="http://110.16.70.26/nmjgpublisher/handle/ProjectsInfoHandler.ashx?type=CorpInfo&lblPageCount=38&lblPageIndex={}&lblRowsCount=757&lblPageSize=20&SFZBDL=&CorpName=&Zzlx=&CertNum=&City=&_=1565252583301".format(page)
            yield Request(url,callback=self.parse_conmanylist)
        #备案
        if response.url == 'http://110.16.70.26/nmjgpublisher/handle/ProjectsInfoHandler.ashx?type=CorpInfoQW&SFZBDL=&CorpName=&Zzlx=&CertNum=&City=&nPageIndex=1&nPageCount=0&nPageRowsCount=0&nPageSize=20':
            tb = json.loads(response.text).get("tb")
            tree = etree.HTML(tb)
            tr_list = tree.xpath("//tr")
            if tr_list:
                for tr in tr_list:
                    beian = BeianItem()
                    beian["social_credit_code"] = tr.xpath("./td[3]/text()")[0]
                    beian["company_name"] = tr.xpath("./td[2]/a/text()")[0]
                    beian["record_province"] = "内蒙古"
                    yield beian
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
        c_info = CompanyInfomortation()
        c_info["province_company_id"] = "neimenggu_" + response.meta.get("CorpCode")
        c_info["company_name"] =response.meta.get("CorpName")
        c_info["social_credit_code"] =response.meta.get("CorpCode")
        c_info["leal_person"] =str(response.xpath("//div[@class='basic_infor']/table/tr[3]/td[2]/text()").extract_first()).strip()
        c_info["regis_type"] =str(response.xpath("//div[@class='basic_infor']/table/tr[4]/td[2]/text()").extract_first()).strip()
        c_info["contact_person"] =str(response.xpath("//div[@class='basic_infor']/table/tr[5]/td[2]/text()").extract_first()).strip()
        c_info["contact_address"] =str(response.xpath("//div[@class='basic_infor']/table/tr[6]/td[2]/text()").extract_first()).strip()
        try:
            c_info["registered_capital"] =str(response.xpath("//div[@class='basic_infor']/table/tr[2]/td[4]/text()").extract_first()).strip().strip("万元(人民币)")
        except:
            c_info["registered_capital"] = str(
                response.xpath("//div[@class='basic_infor']/table/tr[2]/td[4]/text()").extract_first()).strip()
        c_info["leal_person_title"] =str(response.xpath("//div[@class='basic_infor']/table/tr[3]/td[4]/text()").extract_first()).strip()
        c_info["build_date"] =str(response.xpath("//div[@class='basic_infor']/table/tr[4]/td[4]/text()").extract_first()).strip()
        c_info["regis_address"] =str(response.xpath("//div[@class='basic_infor']/table/tr[5]/td[4]/text()").extract_first()).strip() + str(response.xpath("//div[@class='basic_infor']/table/tr[5]/td[6]/text()").extract_first()).strip()
        c_info["leal_person_duty"] =str(response.xpath("//div[@class='basic_infor']/table/tr[3]/td[6]/text()").extract_first()).strip()
        c_info["postalcode"] =str(response.xpath("//div[@class='basic_infor']/table/tr[4]/td[6]/text()").extract_first()).strip()
        c_info["url"] =response.url
        c_info["source"] = "内蒙古"
        yield c_info
        table_list=response.xpath("//table[@class='no_list_table']")
        if table_list:
            for table in table_list:
                c_apt = CompanyaptitudeItem()
                c_apt["province_company_id"] = c_info["province_company_id"]
                c_apt["company_name"] = c_info["company_name"]
                c_apt["aptitude_id"] =str(table.xpath("./tr[1]/td[2]/text()").extract_first()).strip()
                c_apt["aptitude_startime"] =str(table.xpath("./tr[2]/td[2]/text()").extract_first()).strip()
                c_apt["aptitude_name"] =str(table.xpath("./tr[3]/td[2]/text()").extract_first()).strip()
                c_apt["aptitude_organ"] =str(table.xpath("./tr[1]/td[4]/text()").extract_first()).strip()
                c_apt["aptitude_endtime"] =str(table.xpath("./tr[2]/td[4]/text()").extract_first()).strip()
                c_apt["source"] = "内蒙古"
                yield c_apt

    # def parse_beiancompanylist(self,response):
    #     tb = json.loads(response.text).get("tb")
    #     tree = etree.HTML(tb)
    #     tr_list = tree.xpath("//tr")
    #     if tr_list:
    #         for tr in tr_list:
    #             beian = BeianItem()
    #             beian["social_credit_code"] = response.xpath("//div[@class='bottom']/dl[1]/dt/text()").extract_first()
    #             beian["company_name"] = response.xpath("//span[@class='user-name']/text()").extract_first()
    #             beian["record_province"] = "青海"
    #             yield beian
    #             company_url = tr.xpath("./td[2]/a/@onclick")[0]
    #             CorpCode = company_url.split("'")[1]
    #             CorpName = company_url.split("'")[3]
    #             RecordGuid= company_url.split("'")[5]

                #yield Request(company_url, callback=self.parse_beiancompany, meta={"CorpCode": CorpCode, "CorpName": CorpName})
    # def parse_beiancompany(self,response):
    #     beian = BeianItem()
    #     beian["corpcode"] = response.meta.get("CorpCode")
    #     beian["corpname"] =str(response.xpath("//table[@class='cpd_basic_table']/tr[1]/td[2]/text()").extract_first()).strip()
    #     beian["areaname"] =str(response.xpath("//table[@class='cpd_basic_table']/tr[5]/td[6]/text()").extract_first()).strip()
    #     beian["certcode"] = str(response.xpath("//table[@class='cpd_basic_table']/tr[2]/td[2]/text()").extract_first()).strip()
    #     try:
    #         beian["regprin"] = str(response.xpath("//table[@class='cpd_basic_table']/tr[2]/td[4]/text()").extract_first()).strip().strip("万元(人民币)")
    #     except:
    #         beian["regprin"] = str(response.xpath("//table[@class='cpd_basic_table']/tr[2]/td[4]/text()").extract_first()).strip()
    #     beian["legalman"] = str(response.xpath("//table[@class='cpd_basic_table']/tr[3]/td[2]/text()").extract_first()).strip()
    #     beian["legalmanprotitle"] = str(response.xpath("//table[@class='cpd_basic_table']/tr[3]/td[4]/text()").extract_first()).strip()
    #     beian["legalmanduty"] = str(response.xpath("//table[@class='cpd_basic_table']/tr[3]/td[6]/text()").extract_first()).strip()
    #     beian["economicnum"] = str(response.xpath("//table[@class='cpd_basic_table']/tr[4]/td[2]/text()").extract_first()).strip()
    #     beian["corpbirthdate"] = str(response.xpath("//table[@class='cpd_basic_table']/tr[4]/td[4]/text()").extract_first()).strip()
    #     beian["postalcode"] = str(response.xpath("//table[@class='cpd_basic_table']/tr[4]/td[6]/text()").extract_first()).strip()
    #     beian["linkman"] = str(response.xpath("//table[@class='cpd_basic_table']/tr[5]/td[2]/text()").extract_first()).strip()
    #     beian["address"] = str(response.xpath("//table[@class='cpd_basic_table']/tr[6]/td[2]/text()").extract_first()).strip()
    #     beian["record_province"] = "内蒙古"
    #     beian["create_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #     beian["modification_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #     beian["is_delete"] = 0
    #     yield beian



