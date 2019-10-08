# -*- coding: utf-8 -*-
import datetime
import scrapy
from scrapy import FormRequest, Request
from provinceproject.items import *

class XinjiangSpider(scrapy.Spider):
	name = 'xinjiang'
	custom_settings = {
		'DOWNLOAD_DELAY': '0.1',
		# 'DOWNLOADER_MIDDLEWARES': {'provinceproject.middlewares.AbuyunProxyMiddleware': 543, }
	}
	#allowed_domains = ['jsy.xjjs.gov.cn']
	start_urls = ['http://jsy.xjjs.gov.cn/dataservice/query/comp/list/','http://jsy.xjjs.gov.cn/pub/query/baComp/baCompList']

	def parse(self, response):
		if response.url=="http://jsy.xjjs.gov.cn/dataservice/query/comp/list/":
			data_timer=response.xpath("//b[@class='datatimer']/@data-to").extract_first()
			total_page=int(int(data_timer)/15)+2
			for page in range(1,total_page):
				formdata={
					'$total': data_timer,
					'$reload': '0',
					'$pg': str(page),
					'$pgsz': '15'
				}
				yield FormRequest(response.url,formdata=formdata,callback=self.parse_companylist)
		if response.url=="http://jsy.xjjs.gov.cn/pub/query/baComp/baCompList":
			data_timer=response.xpath("//b[@class='datatimer']/@data-to").extract_first()
			total_page=int(int(data_timer)/15)+2
			for page in range(1,total_page):
				formdata={
					'$total': data_timer,
					'$reload': '0',
					'$pg': str(page),
					'class': 're_entrance_btn formsubmit2',
					'data-url': 'http://jsy.xjjs.gov.cn:80/pub/query/baComp/baCompList',
					'$pgsz': '15',
					'target': '_blank',
				}
				yield FormRequest(response.url,formdata=formdata,callback=self.parse_beian)

	def parse_companylist(self,response):
		tr_list=response.xpath("//table[@class='table_box']/tbody/tr")
		for tr in tr_list:
			company_url="http://jsy.xjjs.gov.cn"+tr.xpath("./@onclick").extract_first().split("'")[1]
			yield Request(url=company_url,callback=self.parse_company)
	def parse_company(self,response):
		c_info = CompanyInfomortation()
		c_info["province_company_id"]= "xinjiang_" + response.url.split("/")[-1]
		c_info["company_name"]=response.xpath("//span[@class='user-name']/text()").extract_first()
		c_info["social_credit_code"]=response.xpath("//div[@class='bottom']/dl[1]/dt/text()").extract_first()
		if c_info["social_credit_code"] is None:
			c_info["social_credit_code"]=response.xpath("//div[@class='bottom']/dl[1]/dd/text()").extract_first()
		c_info["leal_person"]=response.xpath("//div[@class='bottom']/dl[2]/dd/text()").extract_first()
		c_info["regis_type"]=response.xpath("//div[@class='bottom']/dl[3]/dd/text()").extract_first()
		c_info["build_date"]=response.xpath("//div[@class='bottom']/dl[3]/dt/text()").extract_first()
		if c_info["build_date"] is not None:
			c_info["build_date"]=c_info["build_date"].replace("年","-").replace("月","-").strip("日")
		c_info["regis_address"]=response.xpath("//div[@class='bottom']/dl[4]/dd/text()").extract_first()
		c_info["business_address"]=response.xpath("//div[@class='bottom']/dl[5]/dd/text()").extract_first()
		c_info["url"] = response.url
		c_info["source"] = "新疆"
		yield c_info
		ca_url="http://jsy.xjjs.gov.cn/dataservice/query/comp/caDetailList/{}".format(response.url.split("/")[-1])
		yield Request(ca_url,callback=self.parse_aptitude,meta={"province_company_id":c_info["province_company_id"],"company_name":c_info["company_name"]})
	def parse_aptitude(self,response):
		tr_list=response.xpath("//table[@class='pro_table_box tableMerged']/tbody/tr[@class='row']")
		for tr in tr_list:
			c_apt = CompanyaptitudeItem()
			c_apt["province_company_id"] = response.meta.get("province_company_id")
			c_apt["company_name"] = response.meta.get("company_name")
			c_apt["source"] = "新疆"
			c_apt["aptitude_name"]=str(tr.xpath("./td[2]/text()").extract_first()).strip()
			c_apt["aptitude_startime"]=str(tr.xpath("./td[3]/text()").extract_first()).strip()
			if c_apt["aptitude_startime"] is not None:
				c_apt["aptitude_startime"]=c_apt["aptitude_startime"].replace("年","-").replace("月","-").strip("日")
			c_apt["aptitude_id"]=str(tr.xpath("./td[4]/text()").extract_first()).strip()
			c_apt["aptitude_organ"]=str(tr.xpath("./td[5]/text()").extract_first()).strip()
			yield c_apt
	def parse_beian(self,response):
		tr_list=response.xpath("//table[@class='table_box']/tbody/tr")
		for tr in tr_list:
			beian=BeianItem()
			beian["social_credit_code"]=tr.xpath("./td[2]/text()").extract_first()
			beian["company_name"]=tr.xpath("./td[3]/text()").extract_first()
			beian["record_province"]="新疆"
			yield beian



