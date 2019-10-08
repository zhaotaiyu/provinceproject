# -*- coding: utf-8 -*-
import scrapy
from scrapy import FormRequest,Request
import json
from provinceproject.items import *
import datetime
class HunanSpider(scrapy.Spider):
	name = 'hunan'
	custom_settings = {
		'DOWNLOAD_DELAY': '1',
		'DOWNLOADER_MIDDLEWARES': {'provinceproject.middlewares.AbuyunProxyMiddleware': 543, }
	}
	#allowed_domains = ['gcxm.hunanjs.gov.cn/dataservice.html?queryType=0']
	start_urls = ['http://gcxm.hunanjs.gov.cn/AjaxHandler/PersonHandler.ashx?method=GetListPage&type=1&corptype_1=&corpname_1=&licensenum_1=&Province_1=430000&City_1=&county_1=&persontype=&persontype_2=&personname_2=&idcard_2=&certnum_2=&corpname_2=&prjname_3=&corpname_3=&prjtype_3=&cityname_3=&year_4=&jidu_4=&corpname_4=&corpname_5=&corpcode_5=&legalman_5=&cityname_5=&SafeNum_6=&corpname_6=&pageSize=30&pageIndex=1','http://gcxm.hunanjs.gov.cn/AjaxHandler/PersonHandler.ashx?method=GetListPage&type=5&corptype_1=&corpname_1=&licensenum_1=&Province_1=430000&City_1=&county_1=&persontype=&persontype_2=&personname_2=&idcard_2=&certnum_2=&corpname_2=&prjname_3=&corpname_3=&prjtype_3=&cityname_3=&year_4=2019&jidu_4=2&corpname_4=&corpname_5=&corpcode_5=&legalman_5=&cityname_5=&SafeNum_6=&corpname_6=&pageSize=30&pageIndex=1']

	def parse(self, response):
		if json.loads(response.text).get("success"):
			total_page = json.loads(response.text).get("data").get("pages")
			for page in range(1,int(total_page)+1):
			#for page in range(1, 11):
				url='='.join(response.url.split("=")[0:-1])+"="+str(page)
				yield Request(url,callback=self.parse_companylist,dont_filter=True,meta={'dont_redirect': True})
		else:
			yield Request(response.url, callback=self.parse,dont_filter=True,meta={'dont_redirect': True})
	def parse_companylist(self,response):
		ty = response.url.split("&")[1]
		data_list = json.loads(response.text).get("data").get("list")
		mark = json.loads(response.text).get("success")
		if mark:
			if ty == "type=1":
				for li in data_list:
					company_url = "http://gcxm.hunanjs.gov.cn/AjaxHandler/PersonHandler.ashx?method=getCorpDetail&corpid={}&isout=".format(
						li.get("corpid"))
					yield Request(company_url, callback=self.parse_company, meta={"corpid": li.get("corpid"), "ty": ty,'dont_redirect': True})
			if ty == "type=5":
				for li in data_list:
					beian = BeianItem()
					beian["company_name"] = li.get("corpname")
					beian["social_credit_code"] = li.get("corpcode")
					beian["record_province"] = "湖南"
					yield beian
					# company_url = "http://gcxm.hunanjs.gov.cn/AjaxHandler/PersonHandler.ashx?method=getCorpDetail&corpid={}&isout=1".format(
					# 	li.get("corpid"))
					# yield Request(company_url, callback=self.parse_company, meta={"corpid": li.get("corpid"), "ty": ty})
		else:
			yield Request(response.url,callback=self.parse_companylist,dont_filter=True,meta={'dont_redirect': True})
	def parse_company(self,response):
		mark = json.loads(response.text).get("success")
		if mark:
			ty = response.meta.get("ty")
			data = json.loads(response.text).get("data")
			ds_list = data.get("ds")
			# if ty =="type=1":
			for ds in ds_list[0:1]:
				c_info = CompanyInfomortation()
				c_info["province_company_id"] = "hunan_" + str(response.meta.get("corpid"))
				c_info["company_name"] = ds.get("corpname")
				c_info["social_credit_code"] = ds.get("corpcode")
				c_info["leal_person"] = ds.get("legalman")
				c_info["regis_type"] = ds.get("econtypename")
				c_info["regis_address"] = ds.get("county")
				c_info["business_address"] = ds.get("address")
				c_info["url"] = response.url
				c_info["source"] = "湖南"
				yield c_info
				ds1_list = data.get("ds1")
				if ds1_list:
					for ds1 in ds1_list:
						c_apt = CompanyaptitudeItem()
						c_apt["province_company_id"] = c_info["province_company_id"]
						c_apt["company_name"] = c_info["company_name"]
						c_apt["source"] = "湖南"
						c_apt["aptitude_type"] = ds1.get("aptitudekindname")
						c_apt["aptitude_id"] = ds1.get("certid")
						c_apt["aptitude_name"] = ds1.get("mark")
						c_apt["aptitude_startime"] = ds1.get("organdate")
						c_apt["aptitude_endtime"] = ds1.get("enddate")
						if c_apt["aptitude_startime"]:
							c_apt["aptitude_startime"] = c_apt["aptitude_startime"].strip("T00:00:00")
							c_apt["aptitude_endtime"] = ds1.get("enddate")
						if c_apt["aptitude_endtime"]:
							c_apt["aptitude_endtime"] = c_apt["aptitude_endtime"].strip("T00:00:00")
							c_apt["aptitude_organ"] = ds1.get("organname")
						yield c_apt
			# if ty =="type=5":
			# 	for ds in ds_list:
			# 		beian = BeianItem()
			# 		beian["company_name"] = ds.get("corpname")
			# 		beian["social_credit_code"] = ds.get("corpcode")
			# 		beian["record_province"] = "湖南"
			# 		yield beian
		else:
			yield Request(response.url, callback=self.parse_company, dont_filter=True)



		



