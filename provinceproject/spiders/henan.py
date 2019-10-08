# -*- coding: utf-8 -*-
import scrapy,datetime
from scrapy import Request,FormRequest
from provinceproject.items import *


class HenanSpider(scrapy.Spider):
	name = 'henan'
	custom_settings = {
		'DOWNLOAD_DELAY': '0.1',
		# 'DOWNLOADER_MIDDLEWARES': {'provinceproject.middlewares.AbuyunProxyMiddleware': 543, }
	}
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
		c_info = CompanyInfomortation()
		c_info["province_company_id"] = "henan_" + response.meta.get("CorpCode")
		c_info["company_name"] = str(response.xpath("//table[@class='Tab']/tr[2]/td[2]/span/text()").extract_first()).strip()
		c_info["regis_address"] = str(response.xpath("//table[@class='Tab']/tr[3]/td[2]/span/text()").extract_first()).strip()
		c_info["build_date"] = str(response.xpath("//table[@class='Tab']/tr[4]/td[2]/span/text()").extract_first()).strip()
		c_info["business_address"] = str(response.xpath("//table[@class='Tab']/tr[5]/td[2]/span/text()").extract_first()).strip()
		c_info["leal_person"] = str(response.xpath("//table[@class='Tab']/tr[6]/td[2]/span/text()").extract_first()).strip()
		c_info["contact_person"] = str(response.xpath("//table[@class='Tab']/tr[7]/td[2]/span/text()").extract_first()).strip()
		c_info["social_credit_code"] = response.xpath("//table[@class='Tab']/tr[2]/td[4]/span/text()").extract_first()
		if not c_info["social_credit_code"]:
			c_info["social_credit_code"] = str(response.xpath("//table[@class='Tab']/tr[4]/td[4]/span/text()").extract_first()).strip()
		else:
			c_info["social_credit_code"] = str(c_info["social_credit_code"]).strip()
		c_info["regis_type"] = str(response.xpath("//table[@class='Tab']/tr[3]/td[4]/span/text()").extract_first()).strip()
		c_info["postalcode"] = str(response.xpath("//table[@class='Tab']/tr[5]/td[4]/span/text()").extract_first()).strip()
		c_info["leal_person_duty"] = str(response.xpath("//table[@class='Tab']/tr[6]/td[4]/span/text()").extract_first()).strip()
		c_info["website"] = str(response.xpath("//table[@class='Tab']/tr[7]/td[4]/span/text()").extract_first()).strip()
		c_info["url"] = response.url
		c_info["source"] = "河南"
		yield c_info
		aptitude_url = "http://hngcjs.hnjs.gov.cn/SiKuWeb/Qyzz.aspx?corpname={}&CorpCode={}".format(response.meta.get("CorpName"),response.meta.get("CorpCode"))
		yield Request(aptitude_url,callback=self.parse_aptitude,meta={"province_company_id":c_info["province_company_id"],"company_name":c_info["company_name"]})
	def parse_aptitude(self,response):
		table_list = response.xpath("//table[@class='Tab']")
		if table_list:
			for table in table_list:
				c_apt = CompanyaptitudeItem()
				c_apt["province_company_id"] = response.meta.get("province_company_id")
				c_apt["company_name"] = response.meta.get("company_name")
				c_apt["source"] = "河南"
				c_apt["aptitude_type"] = str(table.xpath("./tr[1]/td/span/text()").extract_first()).strip()
				c_apt["aptitude_id"] = str(table.xpath("./tr[2]/td[2]/span/text()").extract_first()).strip()
				c_apt["aptitude_startime"] = str(table.xpath("./tr[3]/td[2]/span/text()").extract_first()).strip()
				c_apt["aptitude_name"] = str(table.xpath("./tr[4]/td[2]/span/text()").extract_first()).strip()
				c_apt["aptitude_organ"] = str(table.xpath("./tr[2]/td[4]/span/text()").extract_first()).strip()
				c_apt["aptitude_endtime"] = str(table.xpath("./tr[3]/td[4]/span/text()").extract_first()).strip()
				yield c_apt


