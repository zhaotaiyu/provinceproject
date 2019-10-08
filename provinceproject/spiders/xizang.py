# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from provinceproject.items import *
import datetime

class XizangSpider(scrapy.Spider):
	name = 'xizang'
	custom_settings = {
		'DOWNLOAD_DELAY': '0.1',
		# 'DOWNLOADER_MIDDLEWARES': {'provinceproject.middlewares.AbuyunProxyMiddleware': 543, }
	}
	#allowed_domains = ['111.11.196.111/aspx/corpinfo/CorpInfo.aspx']
	start_urls = ['http://111.11.196.111/aspx/corpinfo/CorpInfo.aspx/']
	def parse(self, response):
		total_page=response.xpath("//span[@id='pagecountCtrl']/text()").extract_first()
		for page in range(1,int(total_page)+1):
			url="http://111.11.196.111/aspx/corpinfo/CorpInfo.aspx?corpname=&cert=&PageIndex={}".format(page)
			yield Request(url,callback=self.parse_companylist)
	def parse_companylist(self,response):
		tr_list=response.xpath("//table[@class='table table-striped table-bordered']/tbody/tr")
		if tr_list:
			for tr in tr_list:
				company_url=tr.xpath("./td[2]/a/@href").extract_first()
				if company_url:
					company_url="http://111.11.196.111/aspx/corpinfo/CorpDetailInfo.aspx?"+company_url.split("?")[-1]
					yield Request(company_url,callback=self.parse_company)
	def parse_company(self,response):
		c_info = CompanyInfomortation()
		c_info["province_company_id"] = "xizang_" + response.url.split("=")[-1]
		c_info["company_name"] =response.xpath("//div[@class='col-sm-12']/table/tbody/tr[1]/td[2]/text()").extract_first()
		c_info["leal_person"] =response.xpath("//div[@class='col-sm-12']/table/tbody/tr[3]/td[2]/text()").extract_first()
		c_info["regis_type"] =response.xpath("//div[@class='col-sm-12']/table/tbody/tr[4]/td[2]/text()").extract_first()
		c_info["contact_person"] =response.xpath("//div[@class='col-sm-12']/table/tbody/tr[5]/td[2]/text()").extract_first()
		c_info["contact_address"] =response.xpath("//div[@class='col-sm-12']/table/tbody/tr[6]/td[2]/text()").extract_first()
		c_info["registered_capital"] =response.xpath("//div[@class='col-sm-12']/table/tbody/tr[2]/td[4]/span[@id='regmoney']/text()").extract_first()
		c_info["leal_person_title"] =response.xpath("//div[@class='col-sm-12']/table/tbody/tr[3]/td[4]/text()").extract_first()
		c_info["build_date"] =response.xpath("//div[@class='col-sm-12']/table/tbody/tr[4]/td[4]/text()").extract_first()
		c_info["regis_address"] =str(response.xpath("//div[@class='col-sm-12']/table/tbody/tr[5]/td[4]/text()").extract_first()) + str(response.xpath("//div[@class='col-sm-12']/table/tbody/tr[5]/td[6]/text()").extract_first())
		c_info["social_credit_code"] =response.xpath("//div[@class='col-sm-12']/table/tbody/tr[2]/td[6]/text()").extract_first()
		if c_info["social_credit_code"] is None:
			c_info["social_credit_code"]=response.xpath("//div[@class='col-sm-12']/table/tbody/tr[2]/td[2]/text()").extract_first()
		c_info["leal_person_duty"] =response.xpath("//div[@class='col-sm-12']/table/tbody/tr[3]/td[6]/text()").extract_first()
		c_info["postalcode"] =response.xpath("//div[@class='col-sm-12']/table/tbody/tr[4]/td[6]/text()").extract_first()
		c_info["url"] =response.url
		c_info["source"] = "西藏"
		yield c_info
		table_list=response.xpath("//div[@id='company_info_zizhi']/table")
		if table_list:
			for table in table_list:
				c_apt = CompanyaptitudeItem()
				c_apt["province_company_id"] = c_info["province_company_id"]
				c_apt["company_name"] = c_info["company_name"]
				c_apt["source"] = "西藏"
				c_apt["aptitude_id"] =table.xpath("./tbody/tr[1]/td[2]/text()").extract_first()
				c_apt["aptitude_startime"] =table.xpath("./tbody/tr[2]/td[2]/text()").extract_first()
				c_apt["aptitude_name"] =table.xpath("./tbody/tr[3]/td[2]/text()").extract_first()
				c_apt["aptitude_organ"] =table.xpath("./tbody/tr[1]/td[4]/text()").extract_first()
				c_apt["aptitude_endtime"] =table.xpath("./tbody/tr[2]/td[4]/text()").extract_first()
				yield c_apt

