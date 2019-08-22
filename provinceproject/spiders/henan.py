# -*- coding: utf-8 -*-
import scrapy,datetime
from scrapy import Request,FormRequest
from provinceproject.items import *


class HenanSpider(scrapy.Spider):
	name = 'henan'
	#allowed_domains = ['hngcjs.hnjs.gov.cn/SiKuWeb/QiyeList.aspx?type=qyxx']
	start_urls = ['http://hngcjs.hnjs.gov.cn/SiKuWeb/QiyeList.aspx?type=qyxx']

	def parse(self, response):
		now_page = int(response.xpath("//div[@id='AspNetPager2']/ul/li//span[@class='active']/text()").extract_first())
		total_page = int(response.xpath("//div[@id='AspNetPager2']/ul/li[13]/a/text()").extract_first())
		__VIEWSTATE = response.xpath("//input[@id='__VIEWSTATE']/@value").extract_first()
		__EVENTVALIDATION = response.xpath("//input[@id='__EVENTVALIDATION']/@value").extract_first()
		__VIEWSTATEGENERATOR = response.xpath("//input[@id='__VIEWSTATEGENERATOR']/@value").extract_first()
		for page in range(1,total_page+1):
			formdata = {
				'__EVENTTARGET':'AspNetPager2',
				'__EVENTARGUMENT':str(page),
				'__VIEWSTATE':__VIEWSTATE,
				'__VIEWSTATEGENERATOR':__VIEWSTATEGENERATOR,
				'__EVENTVALIDATION':__EVENTVALIDATION,
				'CretType':'全部企业类别',
			}
			yield FormRequest(response.url,formdata=formdata,callback=self.parse_companylist)
	def parse_companylist(self,response):
		tr_list = response.xpath("//div[@id='tagContenth0']/table/tbody/tr")
		for tr in tr_list[1:]:
			CorpName = tr.xpath("./td[2]/a/text()").extract_first()
			CorpCode = tr.xpath("./td[3]/text()").extract_first()
			company_url = "http://hngcjs.hnjs.gov.cn/SiKuWeb/QiyeDetail.aspx?CorpName={}&CorpCode={}".format(CorpName,CorpCode)
			yield Request(company_url,callback=self.parse_company,meta={"CorpCode":CorpCode,"CorpName":CorpName})

	def parse_company(self,response):
		henan = HenanItem()
		henan["id"] = response.meta.get("CorpCode")
		henan["name"] = str(response.xpath("//table[@class='Tab']/tr[2]/td[2]/span/text()").extract_first()).strip()
		henan["reg_address"] = str(response.xpath("//table[@class='Tab']/tr[3]/td[2]/span/text()").extract_first()).strip()
		henan["build_date"] = str(response.xpath("//table[@class='Tab']/tr[4]/td[2]/span/text()").extract_first()).strip()
		henan["address"] = str(response.xpath("//table[@class='Tab']/tr[5]/td[2]/span/text()").extract_first()).strip()
		henan["leal_person"] = str(response.xpath("//table[@class='Tab']/tr[6]/td[2]/span/text()").extract_first()).strip()
		henan["contact_person"] = str(response.xpath("//table[@class='Tab']/tr[7]/td[2]/span/text()").extract_first()).strip()
		henan["social_credit_code"] = response.xpath("//table[@class='Tab']/tr[2]/td[4]/span/text()").extract_first()
		if not henan["social_credit_code"]:
			henan["social_credit_code"] = str(response.xpath("//table[@class='Tab']/tr[4]/td[4]/span/text()").extract_first()).strip()
		else:
			henan["social_credit_code"] = str(henan["social_credit_code"]).strip()
		henan["regis_type"] = str(response.xpath("//table[@class='Tab']/tr[3]/td[4]/span/text()").extract_first()).strip()
		henan["postalcode"] = str(response.xpath("//table[@class='Tab']/tr[5]/td[4]/span/text()").extract_first()).strip()
		henan["tech_lead_duty"] = str(response.xpath("//table[@class='Tab']/tr[6]/td[4]/span/text()").extract_first()).strip()
		henan["website"] = str(response.xpath("//table[@class='Tab']/tr[7]/td[4]/span/text()").extract_first()).strip()
		henan["url"] = response.url
		henan["create_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		henan["modification_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		henan["is_delete"] = 0
		aptitude_url = "http://hngcjs.hnjs.gov.cn/SiKuWeb/Qyzz.aspx?corpname={}&CorpCode={}".format(response.meta.get("CorpName"),response.meta.get("CorpCode"))
		yield Request(aptitude_url,callback=self.parse_aptitude,meta={"henan":henan})
	def parse_aptitude(self,response):
		henan =response.meta.get("henan")
		table_list = response.xpath("//table[@class='Tab']")
		if table_list:
			for table in table_list:
				henan["aptitude_type"] = str(table.xpath("./tr[1]/td/span/text()").extract_first()).strip()
				henan["aptitude_num"] = str(table.xpath("./tr[2]/td[2]/span/text()").extract_first()).strip()
				henan["aptitude_accept_date"] = str(table.xpath("./tr[3]/td[2]/span/text()").extract_first()).strip()
				henan["aptitude_range"] = str(table.xpath("./tr[4]/td[2]/span/text()").extract_first()).strip()
				henan["aptitude_organ"] = str(table.xpath("./tr[2]/td[4]/span/text()").extract_first()).strip()
				henan["aptitude_useful_date"] = str(table.xpath("./tr[3]/td[4]/span/text()").extract_first()).strip()
				yield henan
				
		else:
			yield henan

