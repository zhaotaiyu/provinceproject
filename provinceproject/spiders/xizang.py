# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from provinceproject.items import *
import datetime

class XizangSpider(scrapy.Spider):
	name = 'xizang'
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
		xizang=XizangItem()
		xizang["id"] = response.url.split("=")[-1]
		xizang["name"] =response.xpath("//div[@class='col-sm-12']/table/tbody/tr[1]/td[2]/text()").extract_first()
		xizang["leal_person"] =response.xpath("//div[@class='col-sm-12']/table/tbody/tr[3]/td[2]/text()").extract_first()
		xizang["regis_type"] =response.xpath("//div[@class='col-sm-12']/table/tbody/tr[4]/td[2]/text()").extract_first()
		xizang["contact_person"] =response.xpath("//div[@class='col-sm-12']/table/tbody/tr[5]/td[2]/text()").extract_first()
		xizang["contact_address"] =response.xpath("//div[@class='col-sm-12']/table/tbody/tr[6]/td[2]/text()").extract_first()
		xizang["registered_capital"] =response.xpath("//div[@class='col-sm-12']/table/tbody/tr[2]/td[4]/span[@id='regmoney']/text()").extract_first()
		xizang["leal_person_title"] =response.xpath("//div[@class='col-sm-12']/table/tbody/tr[3]/td[4]/text()").extract_first()
		xizang["build_date"] =response.xpath("//div[@class='col-sm-12']/table/tbody/tr[4]/td[4]/text()").extract_first()
		xizang["reg_address_province"] =response.xpath("//div[@class='col-sm-12']/table/tbody/tr[5]/td[4]/text()").extract_first()
		xizang["social_credit_code"] =response.xpath("//div[@class='col-sm-12']/table/tbody/tr[2]/td[6]/text()").extract_first()
		if xizang["social_credit_code"] is None:
			xizang["social_credit_code"]=response.xpath("//div[@class='col-sm-12']/table/tbody/tr[2]/td[2]/text()").extract_first()
		xizang["leal_person_duty"] =response.xpath("//div[@class='col-sm-12']/table/tbody/tr[3]/td[6]/text()").extract_first()
		xizang["postalcode"] =response.xpath("//div[@class='col-sm-12']/table/tbody/tr[4]/td[6]/text()").extract_first()
		xizang["reg_address_city"] =response.xpath("//div[@class='col-sm-12']/table/tbody/tr[5]/td[6]/text()").extract_first()
		xizang["url"] =response.url
		xizang["create_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		xizang["modification_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		xizang["is_delete"] = 0
		table_list=response.xpath("//div[@id='company_info_zizhi']/table")
		if table_list:
			for table in table_list:
				xizang["aptitude_num"] =table.xpath("./tbody/tr[1]/td[2]/text()").extract_first()
				xizang["aptitude_accept_date"] =table.xpath("./tbody/tr[2]/td[2]/text()").extract_first()
				xizang["aptitude_range"] =table.xpath("./tbody/tr[3]/td[2]/text()").extract_first()
				xizang["aptitude_organ"] =table.xpath("./tbody/tr[1]/td[4]/text()").extract_first()
				xizang["aptitude_useful_date"] =table.xpath("./tbody/tr[2]/td[4]/text()").extract_first()
				xizang["tech_lead"] =table.xpath("./tbody/tr[2]/td[6]/text()").extract_first()
				yield xizang
		else:
			yield xizang

