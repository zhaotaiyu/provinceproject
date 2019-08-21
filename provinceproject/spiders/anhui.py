# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request,FormRequest
from provinceproject.items import *
import json
import datetime

class AnhuiSpider(scrapy.Spider):
	name = 'anhui'
	#allowed_domains = ['dohurd.ah.gov.cn/ahzjt_Front/']
	start_urls = ['http://dohurd.ah.gov.cn/ahzjt_Front']

	def parse(self, response):
		try:
			data = json.loads(response.text).get("all")
			pageindex = int(data.get("pageindex",0))
			total_page = int(data.get("total",0))
			listinfo = data.get("listinfo")
			for info in listinfo:
				rowguid = info.get("rowguid")
				company_url = "http://dohurd.ah.gov.cn/epoint-mini/rest/function/searchQYXQYM"
				c_formdata = {
					'rowguid': rowguid
				}
				yield FormRequest(company_url,formdata = c_formdata,callback = self.parse_company,meta = {"rowguid":rowguid})
		except:
			pageindex = 0
			total_page = 2
		if pageindex < total_page:
			url = "http://61.190.70.122:8003/epoint-mini/rest/function/searchSNQY"
			formdata = {
				'pagesize': '12',
				'pageindex': str(pageindex+1),
				'type': '2',
				'txt1': '',
				'CorpCode':'',
				'CorpName': '',
				'LegalMan': '',
				'CertTypeNum': '',
				'AreaCode': '',
			}
			yield FormRequest(url,formdata = formdata,callback = self.parse)

	def parse_company(self,response):
		ds = json.loads(response.text).get("QYXQ")
		if ds:
			anhui = AnhuiItem()
			anhui["id"] = response.meta.get("rowguid")
			anhui["name"] = ds.get("corpname")
			anhui["social_credit_code"] = ds.get("corpcode")
			anhui["leal_person"] = ds.get("legalman")
			anhui["regis_type"] = ds.get("economicnumtext")
			anhui["reg_address"] = ds.get("areacodetext")
			anhui["address"] = ds.get("address")
			anhui["url"] = response.url
			anhui["create_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
			anhui["modification_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
			anhui["is_delete"] = 0
			aptitude_url = "http://dohurd.ah.gov.cn/epoint-mini/rest/function/searchQYXQ"
			formdata = {
				'pagesize': '99',
				'pageindex': '1',
				'corpcode': ds.get("corpcode"),
				'PageType': '',
			}
			yield FormRequest(aptitude_url,formdata = formdata,callback = self.parse_aptitude,meta = {"anhui":anhui})
	def parse_aptitude(self,response):
		anhui = response.meta.get("anhui")
		data = json.loads(response.text).get("all")
		ds1_list = data.get("listinfo")
		if ds1_list:
			for ds1 in ds1_list:
				anhui["aptitude_type"] = ds1.get("certtypenumtext")
				anhui["aptitude_num"] = ds1.get("certid")
				anhui["aptitude_range"] = ds1.get("certname")
				anhui["aptitude_useful_date"] = ds1.get("enddate")
				anhui["aptitude_organ"] = ds1.get("organname")
				yield anhui

		else:
			yield anhui

