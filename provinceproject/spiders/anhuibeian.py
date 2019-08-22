# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request,FormRequest
from provinceproject.items import *
import json
import datetime

class AnhuibeianSpider(scrapy.Spider):
	name = 'anhuibeian'
	#allowed_domains = ['dohurd.ah.gov.cn/ahzjt_Front']
	start_urls = ['http://dohurd.ah.gov.cn/ahzjt_Front/']

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
			url = "http://61.190.70.122:8003/epoint-mini/rest/function/searchSWQY"
			formdata = {
				'pagesize': '12',
				'pageindex': str(pageindex+1),
				'type': '2',
				'txt1': '',
				'CorpCode':'',
				'CorpName': '',
				'LegalMan': '',
				'CertTypeNum': 'null',
				'AreaCode': '',
			}
			yield FormRequest(url,formdata = formdata,callback = self.parse)

	def parse_company(self,response):
		ds = json.loads(response.text).get("QYXQ")
		if ds:
			beian = BeianItem()
			beian["corpname"] = ds.get("corpname")
			beian["corpcode"] = ds.get("corpcode")
			beian["legalman"] = ds.get("legalman")
			beian["danweitype"] = ds.get("economicnumtext")
			beian["areaname"] = ds.get("areacodetext")
			beian["record_province"] = "安徽"
			beian["create_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
			beian["modification_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
			beian["is_delete"] = 0
			yield beian

