# -*- coding: utf-8 -*-
import scrapy
from scrapy import FormRequest,Request
from provinceproject.items import *
import datetime

class BeijingSpider(scrapy.Spider):
	name = 'beijing'
	custom_settings = {
		'DOWNLOAD_DELAY': '0.5',
		# 'DOWNLOADER_MIDDLEWARES' : {'provinceproject.middlewares.AbuyunProxyMiddleware': 543}
	}
	#allowed_domains = ['www.bjjs.gov.cn/eportal/ui?pageId=307900']
	start_urls = ['http://zjw.beijing.gov.cn/eportal/ui?pageId=307900']

	def parse(self, response):
		total_num=response.xpath("//td[@class='Normal']/text()[2]").extract_first().strip().split(":")[1].split(",")[0]
		url="http://zjw.beijing.gov.cn/eportal/ui?pageId=307900"
		for page in range(1,int(int(total_num)/15)+2):
			formdata={
				'currentPage': str(page),
				'pageSize': '15'
			}
			yield FormRequest(url,formdata=formdata,callback=self.parse_companylist)
	def parse_companylist(self,response):
		tr_list=response.xpath("//table[@id='tab_view']/tbody/tr")
		if tr_list:
			for tr in tr_list[1:]:
				company_url = tr.xpath("./td[3]/a/@href").extract_first()
				if company_url:
					company_url="http://zjw.beijing.gov.cn"+company_url
					yield Request(company_url,callback=self.parse_company)
	def parse_company(self,response):
		beijing = BeijingItem()
		beijing["id"] = response.url.split("=")[-1]
		beijing["name"] = str(response.xpath("//table[@class='detailview']/tbody/tr[1]/td[2]/text()").extract_first()).strip()
		beijing["address"] = str(response.xpath("//table[@class='detailview']/tbody/tr[2]/td[2]/text()").extract_first()).strip()
		beijing["registered_capital"] = str(response.xpath("//table[@class='detailview']/tbody/tr[3]/td[2]/text()").extract_first()).strip().strip("欧美日人民币(万元)")
		beijing["social_credit_code"] = str(response.xpath("//table[@class='detailview']/tbody/tr[4]/td[2]/text()").extract_first()).strip()
		beijing["regis_type"] = str(response.xpath("//table[@class='detailview']/tbody/tr[5]/td[2]/text()").extract_first()).strip()
		beijing["leal_person"] = str(response.xpath("//table[@class='detailview']/tbody/tr[6]/td[2]/text()").extract_first()).strip()
		beijing["aptitude_num"] = str(response.xpath("//table[@class='detailview']/tbody/tr[7]/td[2]/text()").extract_first()).strip()
		beijing["aptitude_range"] = str(response.xpath("//table[@class='detailview']/tbody/tr[8]/td[2]/text()").extract_first()).strip()
		beijing["aptitude_organ"] = str(response.xpath("//table[@class='detailview']/tbody/tr[9]/td[2]/text()").extract_first()).strip()
		beijing["aptitude_accept_date"] = response.xpath("//table[@class='detailview']/tbody/tr[10]/td[2]/span[1]/text()").extract_first()
		beijing["aptitude_useful_date"] = response.xpath("//table[@class='detailview']/tbody/tr[10]/td[2]/span[2]/text()").extract_first()
		beijing["url"] = response.url
		beijing["create_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		beijing["modification_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		beijing["is_delete"]=0
		yield beijing
