# -*- coding: utf-8 -*-
import datetime
import scrapy
from scrapy import FormRequest, Request
from provinceproject.items import *

class XinjiangSpider(scrapy.Spider):
	name = 'xinjiang'
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
		xinjiang=XinjiangItem()
		xinjiang["id"]=response.url.split("/")[-1]
		xinjiang["name"]=response.xpath("//span[@class='user-name']/text()").extract_first()
		xinjiang["social_credit_code"]=response.xpath("//div[@class='bottom']/dl[1]/dt/text()").extract_first()
		if xinjiang["social_credit_code"] is None:
			xinjiang["social_credit_code"]=response.xpath("//div[@class='bottom']/dl[1]/dd/text()").extract_first()
		xinjiang["leal_person"]=response.xpath("//div[@class='bottom']/dl[2]/dd/text()").extract_first()
		xinjiang["regis_type"]=response.xpath("//div[@class='bottom']/dl[3]/dd/text()").extract_first()
		xinjiang["build_date"]=response.xpath("//div[@class='bottom']/dl[3]/dt/text()").extract_first()
		if xinjiang["build_date"] is not None:
			xinjiang["build_date"]=xinjiang["build_date"].replace("年","-").replace("月","-").strip("日")
		xinjiang["reg_address"]=response.xpath("//div[@class='bottom']/dl[4]/dd/text()").extract_first()
		xinjiang["address"]=response.xpath("//div[@class='bottom']/dl[5]/dd/text()").extract_first()
		xinjiang["url"] = response.url
		xinjiang["create_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		xinjiang["modification_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		xinjiang["is_delete"] = 0
		ca_url="http://jsy.xjjs.gov.cn/dataservice/query/comp/caDetailList/{}".format(xinjiang["id"])
		yield Request(ca_url,callback=self.parse_aptitude,meta={"xinjiang":xinjiang})
	def parse_aptitude(self,response):
		xinjiang=response.meta.get("xinjiang")
		tr_list=response.xpath("//table[@class='pro_table_box tableMerged']/tbody/tr[@class='row']")
		for tr in tr_list:
			xinjiang["aptitude_range"]=str(tr.xpath("./td[2]/text()").extract_first()).strip()
			xinjiang["aptitude_accept_date"]=str(tr.xpath("./td[3]/text()").extract_first()).strip()
			if xinjiang["aptitude_accept_date"] is not None:
				xinjiang["aptitude_accept_date"]=xinjiang["aptitude_accept_date"].replace("年","-").replace("月","-").strip("日")
			xinjiang["aptitude_num"]=str(tr.xpath("./td[4]/text()").extract_first()).strip()
			xinjiang["aptitude_organ"]=str(tr.xpath("./td[5]/text()").extract_first()).strip()
			yield xinjiang
	def parse_beian(self,response):
		tr_list=response.xpath("//table[@class='table_box']/tbody/tr")
		for tr in tr_list:
			beian=BeianItem()
			beian["corpcode"]=tr.xpath("./td[2]/text()").extract_first()
			beian["corpname"]=tr.xpath("./td[3]/text()").extract_first()
			beian["areaname"]=tr.xpath("./td[4]/text()").extract_first()
			beian["legalman"]=tr.xpath("./td[5]/text()").extract_first()
			beian["record_province"]="新疆"
			beian["create_time"]=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
			beian["modification_time"]=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
			beian["is_delete"]=0
			yield beian



