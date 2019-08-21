# -*- coding: utf-8 -*-
import datetime
import scrapy
from scrapy import FormRequest,Request
from provinceproject.items import *
class LiaoningSpider(scrapy.Spider):
    name = 'liaoning'
    #allowed_domains = ['218.60.144.163/LNJGPublisher/corpinfo/CorpInfo.aspx']
    start_urls = ['http://218.60.144.163/LNJGPublisher/corpinfo/CorpInfo.aspx/']
    def parse(self, response):
        url = "http://218.60.144.163/LNJGPublisher/corpinfo/CorpInfo.aspx"
        total_page = response.xpath("//div[@id='divPage']/div/p/span[2]/span/text()").extract_first()
        if total_page:
            __VIEWSTATE = response.xpath("//input[@id='__VIEWSTATE']/@value").extract_first()
            __EVENTVALIDATION = response.xpath("//input[@id='__EVENTVALIDATION']/@value").extract_first()
            for page in range(1,int(total_page)+1):
                formdata={
                    '__EVENTTARGET': 'Linkbutton5',
                    '__VIEWSTATE':__VIEWSTATE,
                    '__EVENTVALIDATION':__EVENTVALIDATION,
                    'hidd_type': '1',
                    'newpage': str(page)
                }
                yield FormRequest(url,formdata=formdata,callback=self.parse_companylist)
        beiantotal_page = response.xpath("//div[@id='divPage2']/div/p/span[2]/span/text()").extract_first()
        if beiantotal_page:
            __VIEWSTATE = response.xpath("//input[@id='__VIEWSTATE']/@value").extract_first()
            __EVENTVALIDATION = response.xpath("//input[@id='__EVENTVALIDATION']/@value").extract_first()
            for page in range(1,int(beiantotal_page)+1):
                beianformdata = {
                    '__EVENTTARGET': 'Linkbutton10',
                    '__VIEWSTATE': __VIEWSTATE,
                    '__EVENTVALIDATION': __EVENTVALIDATION,
                    'hidd_type': '2',
                    'newpage': '1',
                    'newpage1': str(page)
                }
                yield FormRequest(url, formdata=beianformdata, callback=self.parse_beiancompanylist)

    def parse_companylist(self,response):
        tr_list=response.xpath("//div[@id='div_Province']/div[1]/table/tbody/tr")
        if tr_list:
            for tr in tr_list:
                company_url=tr.xpath("./td[3]/a/@onclick").extract_first()
                if company_url:
                    rowGuid=company_url.split("'")[1]
                    CorpCode=company_url.split("'")[3]
                    CorpName=company_url.split("'")[5]
                    company_url="http://218.60.144.163/LNJGPublisher/corpinfo/CorpDetailInfo.aspx?rowGuid={}&CorpCode={}&CorpName={}&VType=1".format(rowGuid,CorpCode,CorpName)
                    yield Request(company_url,callback=self.parse_company,meta={"CorpCode":CorpCode,"CorpName":CorpName})
    def parse_company(self,response):
        liaoning=LiaoningItem()
        liaoning["id"] =response.meta.get("CorpCode")
        liaoning["name"] =response.meta.get("CorpName")
        liaoning["social_credit_code"] =str(response.xpath("//table[@class='cpd_basic_table']/tr[2]/td[2]/text()").extract_first()).strip()
        liaoning["leal_person"] =str(response.xpath("//table[@class='cpd_basic_table']/tr[2]/td[2]/text()").extract_first()).strip()
        liaoning["reg_address"] =str(response.xpath("//table[@class='cpd_basic_table']/tr[3]/td[2]/text()").extract_first()).strip()
        liaoning["remark"] =str(response.xpath("//table[@class='cpd_basic_table']/tr[4]/td[2]/text()").extract_first()).strip()
        liaoning["regis_type"] =str(response.xpath("//table[@class='cpd_basic_table']/tr[3]/td[4]/text()").extract_first()).strip()
        liaoning["contact_address"] =str(response.xpath("//table[@class='cpd_basic_table']/tr[4]/td[4]/text()").extract_first()).strip()
        liaoning["url"] = response.url
        liaoning["create_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        liaoning["modification_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        liaoning["is_delete"] = 0
        table_list=response.xpath("//table[@class='no_list_table']")
        if table_list:
            for table in table_list:
                liaoning["aptitude_num"] =str(table.xpath("./tr[1]/td[2]/text()").extract_first()).strip()
                liaoning["aptitude_accept_date"] =str(table.xpath("./tr[2]/td[2]/text()").extract_first()).strip()
                liaoning["aptitude_range"] =str(table.xpath("./tr[3]/td[2]/text()").extract_first()).strip()
                liaoning["aptitude_organ"] =str(table.xpath("./tr[1]/td[4]/text()").extract_first()).strip()
                liaoning["aptitude_useful_date"] =str(table.xpath("./tr[2]/td[4]/text()").extract_first()).strip()
                yield liaoning
        else:
            yield liaoning
#备案企业列表
    def parse_beiancompanylist(self,response):
        tr_list = response.xpath("//div[@id='div_outCast']/div[1]/table/tbody/tr")
        if tr_list:
            for tr in tr_list:
                company_url = tr.xpath("./td[6]/a/@onclick").extract_first()
                if company_url:
                    company_url = "http://218.60.144.163/LNJGPublisher/corpinfo/outCaseCorpDetailInfo.aspx?Fid="+company_url.split("'")[1]
                    yield Request(company_url,callback=self.parse_beiancompany)
    def parse_beiancompany(self,response):
        beian=BeianItem()
        #组织机构代码
        beian["corpcode"]=str(response.xpath("//table[@class='cpd_basic_table']/tr[2]/td[2]/text()").extract_first()).strip()
        #企业名称
        beian["corpname"]=str(response.xpath("//table[@class='cpd_basic_table']/tr[1]/td[2]/text()").extract_first()).strip()
        #注册所在地辖区名称
        beian["areaname"]=str(response.xpath("//table[@class='cpd_basic_table']/tr[4]/td[2]/text()").extract_first()).strip()
        #单位类型
        beian["danweitype"]=str(response.xpath("//table[@class='cpd_basic_table']/tr[12]/td[2]/text()").extract_first()).strip()
        #有效期
        beian["validdate"]=str(response.xpath("//table[@class='cpd_basic_table']/tr[11]/td[2]/text()").extract_first()).strip()
        #法人
        beian["legalman"]=str(response.xpath("//table[@class='cpd_basic_table']/tr[5]/td[2]/text()").extract_first()).strip()
        #技术负责人
        beian["linkman"]=str(response.xpath("//table[@class='cpd_basic_table']/tr[7]/td[2]/text()").extract_first()).strip()
        #技术负责人电话
        beian["linktel"]=str(response.xpath("//table[@class='cpd_basic_table']/tr[8]/td[2]/text()").extract_first()).strip()
        #备案省份
        beian["record_province"]="辽宁"
        #创建时间
        beian["create_time"]=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        #修改时间
        beian["modification_time"]=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        #是否删除
        beian["is_delete"]=0
        yield beian
