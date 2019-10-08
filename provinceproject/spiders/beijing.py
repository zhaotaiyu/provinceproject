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
		c_info  = CompanyInfomortation()
		c_info["province_company_id"] = "beijing_" + response.url.split("=")[-1]
		c_info["company_name"] = str(response.xpath("//table[@class='detailview']/tbody/tr[1]/td[2]/text()").extract_first()).strip()
		c_info["regis_address"] = str(response.xpath("//table[@class='detailview']/tbody/tr[2]/td[2]/text()").extract_first()).strip()
		c_info["registered_capital"] = str(response.xpath("//table[@class='detailview']/tbody/tr[3]/td[2]/text()").extract_first()).strip().strip("欧美日人民币(万元)")
		c_info["social_credit_code"] = str(response.xpath("//table[@class='detailview']/tbody/tr[4]/td[2]/text()").extract_first()).strip()
		c_info["regis_type"] = str(response.xpath("//table[@class='detailview']/tbody/tr[5]/td[2]/text()").extract_first()).strip()
		c_info["leal_person"] = str(response.xpath("//table[@class='detailview']/tbody/tr[6]/td[2]/text()").extract_first()).strip()
		c_info["url"] = response.url
		c_info["source"] = "北京"
		yield c_info
		c_apt = CompanyaptitudeItem()
		c_apt["province_company_id"] = c_info["province_company_id"]
		c_apt["company_name"] = c_info["company_name"]
		c_apt["source"] = "北京"
		c_apt["aptitude_id"] = str(response.xpath("//table[@class='detailview']/tbody/tr[7]/td[2]/text()").extract_first()).strip()
		c_apt["aptitude_name"] = str(response.xpath("//table[@class='detailview']/tbody/tr[8]/td[2]/text()").extract_first()).strip()
		c_apt["aptitude_organ"] = str(response.xpath("//table[@class='detailview']/tbody/tr[9]/td[2]/text()").extract_first()).strip()
		c_apt["aptitude_startime"] = response.xpath("//table[@class='detailview']/tbody/tr[10]/td[2]/span[1]/text()").extract_first()
		c_apt["aptitude_endtime"] = response.xpath("//table[@class='detailview']/tbody/tr[10]/td[2]/span[2]/text()").extract_first()
		yield c_apt
