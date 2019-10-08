# -*- coding: utf-8 -*-
import pymongo

import scrapy
from scrapy import Request,FormRequest
from provinceproject.items import *
import json
import datetime
from ..settings import *

class AnhuiSpider(scrapy.Spider):
	name = 'anhui'
	custom_settings = {
		'DOWNLOAD_DELAY': '0.3',
		'DOWNLOADER_MIDDLEWARES': {'provinceproject.middlewares.AbuyunProxyMiddleware': 543, }
	}
	#allowed_domains = ['dohurd.ah.gov.cn/ahzjt_Front/']
	def start_requests(self):
		url = "http://61.190.70.122:8003/epoint-mini/rest/function/searchSNQY"
		formdata = {
			'pagesize': '12',
			'pageindex': '1',
			'type': '2',
			'txt1': '',
			'CorpCode': '',
			'CorpName': '',
			'LegalMan': '',
			'CertTypeNum': '',
			'AreaCode': '',
		}
		yield FormRequest(url, formdata=formdata, callback=self.parse)
	def parse(self, response):
		try:
			data = json.loads(response.text).get("all")
			pageindex = int(data.get("pageindex",0))
			total = int(data.get("total",2))
			listinfo = data.get("listinfo")
			for info in listinfo:
				rowguid = info.get("rowguid")
				company_url = "http://dohurd.ah.gov.cn/epoint-mini/rest/function/searchQYXQYM"
				c_formdata = {
					'rowguid': rowguid
				}
				yield FormRequest(company_url,formdata = c_formdata,callback = self.parse_company,meta = {"rowguid":rowguid})
			if pageindex * 12 < total:
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
		except:
			self.write_error(response)

	def parse_company(self,response):
		try:
			ds = json.loads(response.text).get("QYXQ")
			if ds:
				c_info = CompanyInfomortation()
				c_info["province_company_id"] = "anhui_" + str(response.meta.get("rowguid"))
				c_info["company_name"] = ds.get("corpname")
				c_info["social_credit_code"] = ds.get("corpcode")
				c_info["leal_person"] = ds.get("legalman")
				c_info["regis_type"] = ds.get("economicnumtext")
				c_info["regis_address"] = ds.get("areacodetext")
				c_info["business_address"] = ds.get("address")
				c_info["url"] = response.url
				c_info["source"] = "安徽"
				yield  c_info
				aptitude_url = "http://dohurd.ah.gov.cn/epoint-mini/rest/function/searchQYXQ"
				formdata = {
					'pagesize': '99',
					'pageindex': '1',
					'corpcode': ds.get("corpcode"),
					'PageType': '',
				}
				yield FormRequest(aptitude_url,formdata = formdata,callback = self.parse_aptitude,meta={"province_company_id":c_info["province_company_id"],"company_name":c_info["company_name"]})
		except:
			self.write_error(response)
	def parse_aptitude(self,response):
		apt_info = CompanyaptitudeItem()
		data = json.loads(response.text).get("all")
		ds1_list = data.get("listinfo")
		if ds1_list:
			for ds1 in ds1_list:
				c_apt = CompanyaptitudeItem()
				c_apt["province_company_id"] = response.meta.get("province_company_id")
				c_apt["company_name"] = response.meta.get("company_name")
				c_apt["source"] = "安徽"
				c_apt["aptitude_type"] = ds1.get("certtypenumtext")
				c_apt["aptitude_id"] = ds1.get("certid")
				c_apt["aptitude_name"] = ds1.get("certname")
				c_apt["aptitude_endtime"] = ds1.get("enddate")
				c_apt["aptitude_organ"] = ds1.get("organname")
				yield c_apt

	def write_error(self, response):
		myclient = pymongo.MongoClient('mongodb://ecs-a025-0002:27017/')
		mydb = myclient[MONGODATABASE]
		mycol = mydb[MONGOTABLE]
		mydict = {"url": response.url, "reason": "该页未返回数据", 'text': response.text, 'spider': 'anhui','headers':response.request.headers.__repr__(),'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
		mycol.insert_one(mydict)
		myclient.close()