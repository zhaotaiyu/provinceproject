# -*- coding: utf-8 -*-
import datetime

import scrapy
from scrapy import FormRequest, Request
from provinceproject.items import *


class HainanSpider(scrapy.Spider):
    name = 'hainan'
    #allowed_domains = ['www.hizj.net:8008']
    start_urls = ['http://www.hizj.net:8008/WebSite_Publish/Default.aspx?action=IntegrityMge/ucCreditCompanyInfoList&Type=建筑业企业资质','http://www.hizj.net:8008/WebSite_Publish/Default.aspx?action=IntegrityMge/ucCreditCompanyInfoList&Type=工程设计企业资质','http://www.hizj.net:8008/WebSite_Publish/Default.aspx?action=IntegrityMge/ucCreditCompanyInfoList&Type=工程监理企业资质','http://www.hizj.net:8008/WebSite_Publish/Default.aspx?action=IntegrityMge/ucCreditCompanyInfoList&Type=工程勘察企业资质','http://www.hizj.net:8008/WebSite_Publish/Default.aspx?action=IntegrityMge/ucCreditCompanyInfoList&Type=工程招标代理机构资质','http://www.hizj.net:8008/WebSite_Publish/Default.aspx?action=IntegrityMge/ucCreditCompanyInfoListZJ&Type=造价咨询企业资质']

    def parse(self, response):
        print(response.url)
        if response.url == 'http://www.hizj.net:8008/WebSite_Publish/Default.aspx?action=IntegrityMge/ucCreditCompanyInfoListZJ&Type=%E9%80%A0%E4%BB%B7%E5%92%A8%E8%AF%A2%E4%BC%81%E4%B8%9A%E8%B5%84%E8%B4%A8':
            total_page = int(response.xpath(
                "//a[@id='ID_IntegrityMge_ucCreditCompanyInfoListZJ_ucPager1_btnLast']/text()").extract_first())
            __VIEWSTATE = response.xpath("//input[@id='__VIEWSTATE']/@value").extract_first()
            __VIEWSTATEGENERATOR = response.xpath("//input[@id='__VIEWSTATEGENERATOR']/@value").extract_first()
            for page in range(1,total_page):
            #for page in range(1, 4):
                formdata = {
                    '__VIEWSTATE': __VIEWSTATE,
                    '__VIEWSTATEGENERATOR': __VIEWSTATEGENERATOR,
                    'ID_IntegrityMge_ucCreditCompanyInfoListZJ$txtProjectName': '',
                    'ID_IntegrityMge_ucCreditCompanyInfoListZJ$ddlProvince': '全部',
                    'ID_IntegrityMge_ucCreditCompanyInfoListZJ$txtValidCode': '',
                    'ID_IntegrityMge_ucCreditCompanyInfoListZJ$ucPager1$txtCurrPage': str(page),
                    'ID_IntegrityMge_ucCreditCompanyInfoListZJ$ucPager1$btnGo': '确定',
                }
                yield FormRequest(response.url, formdata=formdata, callback=self.parse_companylist)
        else:
            total_page = int(response.xpath(
                "//a[@id='ID_IntegrityMge_ucCreditCompanyInfoList_ucPager1_btnLast']/text()").extract_first())
            __VIEWSTATE = response.xpath("//input[@id='__VIEWSTATE']/@value").extract_first()
            __VIEWSTATEGENERATOR = response.xpath("//input[@id='__VIEWSTATEGENERATOR']/@value").extract_first()
            # for page in range(1,total_page):
            for page in range(1, 4):
                formdata = {
                    '__VIEWSTATE':__VIEWSTATE,
                    '__VIEWSTATEGENERATOR': __VIEWSTATEGENERATOR,
                    'ID_IntegrityMge_ucCreditCompanyInfoList$txtProjectName': '',
                    'ID_IntegrityMge_ucCreditCompanyInfoList$ddlProvince': '全部',
                    'ID_IntegrityMge_ucCreditCompanyInfoList$txtValidCode': '',
                    'ID_IntegrityMge_ucCreditCompanyInfoList$ucPager1$txtCurrPage': str(page),
                    'ID_IntegrityMge_ucCreditCompanyInfoList$ucPager1$btnGo': '确定',
                }
                yield FormRequest(response.url,formdata=formdata,callback=self.parse_companylist)
    def parse_companylist(self,response):
        if response.url == 'http://www.hizj.net:8008/WebSite_Publish/Default.aspx?action=IntegrityMge/ucCreditCompanyInfoListZJ&Type=%E9%80%A0%E4%BB%B7%E5%92%A8%E8%AF%A2%E4%BC%81%E4%B8%9A%E8%B5%84%E8%B4%A8':
            tr_list = response.xpath("//table[@id='ID_IntegrityMge_ucCreditCompanyInfoListZJ_gridView']/tr")
            for tr in tr_list[1:]:
                company_url = "http://www.hizj.net:8008/WebSite_Publish/" + tr.xpath("./td[2]/a/@href").extract_first()
                yield Request(company_url, callback=self.parse_zjzxcompany)
        else:
            tr_list = response.xpath("//table[@id='ID_IntegrityMge_ucCreditCompanyInfoList_gridView']/tr")
            for tr in tr_list[1:]:
                company_url = "http://www.hizj.net:8008/WebSite_Publish/" + tr.xpath("./td[2]/a/@href").extract_first()
                yield Request(company_url,callback=self.parse_company)
    def parse_company(self,response):
        hainan = HainanItem()
        hainan["id"] = response.url.split("=")[-1]
        hainan["name"] = response.xpath("//span[@id='ID_IntegrityMge_ucShow_lbCompanyInfoName']/text()").extract_first()
        hainan["social_credit_code"] = response.xpath("//span[@id='ID_IntegrityMge_ucShow_txtOrganization']/text()").extract_first()
        hainan["reg_address"] = response.xpath("//span[@id='ID_IntegrityMge_ucShow_lbProvince']/text()").extract_first() + "-" + response.xpath("//span[@id='ID_IntegrityMge_ucShow_lbCityNum']/text()").extract_first()
        hainan["address"] = response.xpath("//span[@id='ID_IntegrityMge_ucShow_txtAddress']/text()").extract_first()
        hainan["leal_person"] = response.xpath("//span[@id='ID_IntegrityMge_ucShow_txtLegalPerson']/text()").extract_first()
        hainan["registered_capital"] = response.xpath("//span[@id='ID_IntegrityMge_ucShow_txtRegPrin']/text()").extract_first()
        hainan["build_date"] = response.xpath("//span[@id='ID_IntegrityMge_ucShow_txtFoundDate']/text()").extract_first()
        hainan["url"] = response.url
        hainan["create_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        hainan["modification_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        hainan["is_delete"] = 0
        table_list = response.xpath("//center/table")
        for table in table_list:
            hainan["aptitude_type"] = table.xpath("./tr[2]/td/table/tr[2]/td[2]/span/text()").extract_first()
            hainan["aptitude_useful_date"] = table.xpath("./tr[2]/td/table/tr[4]/td[2]/span/text()").extract_first()
            hainan["aptitude_num"] = table.xpath("./tr[2]/td/table/tr[2]/td[4]/span/text()").extract_first()
            hainan["aptitude_accept_date"] = table.xpath("./tr[2]/td/table/tr[3]/td[4]/span/text()").extract_first()
            hainan["aptitude_organ"] = table.xpath("./tr[2]/td/table/tr[4]/td[4]/span/text()").extract_first()
            tr_list = table.xpath(".//table[contains(@id,'_ucCorpCertShow1_DataList')]/tr")
            for tr in tr_list:
                hainan["aptitude_type_b"] = tr.xpath("./td/table/tr[1]/td[2]/span/text()").extract_first()
                hainan["aptitude_level"] = tr.xpath("./td/table/tr[2]/td[2]/span/text()").extract_first()
                hainan["aptitude_type_s"] = tr.xpath("./td/table/tr[1]/td[4]/span/text()").extract_first()
                yield hainan

    #造价咨询企业
    def parse_zjzxcompany(self,response):
        hainan = HainanItem()
        hainan["id"] = response.url.split("=")[-1]
        hainan["name"] = response.xpath("//span[@id='ID_IntegrityMge_ucShowZJ_lbCompanyInfoName']/text()").extract_first()
        hainan["social_credit_code"] = response.xpath("//span[@id='ID_IntegrityMge_ucShowZJ_txtBusinessLicense']/text()").extract_first()
        hainan["reg_address"] = response.xpath("//span[@id='ID_IntegrityMge_ucShowZJ_lbProvince']/text()").extract_first() + "-" + response.xpath("//span[@id='ID_IntegrityMge_ucShowZJ_lbCityNum']/text()").extract_first()

        hainan["address"] = response.xpath("//span[@id='ID_IntegrityMge_ucShowZJ_txtAddress']/text()").extract_first()
        hainan["leal_person"] = response.xpath("//span[@id='ID_IntegrityMge_ucShowZJ_txtLegalPerson']/text()").extract_first()
        hainan["url"] = response.url
        hainan["aptitude_type"] = response.xpath("//span[@id='ID_IntegrityMge_ucShowZJ_ucCorpCertListShow1_listCert_ctl00_ucCorpCertShow1_txtCertTypeNum']/text()").extract_first()
        hainan["aptitude_useful_date"] = response.xpath("//span[@id='ID_IntegrityMge_ucShowZJ_ucCorpCertListShow1_listCert_ctl00_ucCorpCertShow1_txtEndDate']/text()").extract_first()
        hainan["aptitude_num"] = response.xpath("//span[@id='ID_IntegrityMge_ucShowZJ_ucCorpCertListShow1_listCert_ctl00_ucCorpCertShow1_txtCertID']/text()").extract_first()
        hainan["aptitude_accept_date"] = response.xpath("//span[@id='ID_IntegrityMge_ucShowZJ_ucCorpCertListShow1_listCert_ctl00_ucCorpCertShow1_txtOrganDate']/text()").extract_first()
        hainan["aptitude_organ"] = response.xpath("//span[@id='ID_IntegrityMge_ucShowZJ_ucCorpCertListShow1_listCert_ctl00_ucCorpCertShow1_txtOrganName']/text()").extract_first()
        hainan["aptitude_level"] = response.xpath("//span[@id='ID_IntegrityMge_ucShowZJ_ucCorpCertListShow1_listCert_ctl00_ucCorpCertShow1_txtTitleLevelNum']/text()").extract_first()
        hainan["create_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        hainan["modification_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        hainan["is_delete"] = 0
        yield hainan

