# -*- coding: utf-8 -*-
import scrapy
from scrapy import FormRequest,Request
import json
from provinceproject.items import *
import datetime
class HunanSpider(scrapy.Spider):
	name = 'hunan'
	custom_settings = {
		'DOWNLOAD_DELAY': '0.5',
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
				yield Request(url,callback=self.parse_companylist,dont_filter=True)
		else:
			yield Request(response.url, callback=self.parse,dont_filter=True)
	def parse_companylist(self,response):
		ty = response.url.split("&")[1]
		data_list = json.loads(response.text).get("data").get("list")
		mark = json.loads(response.text).get("success")
		if mark:
			if ty == "type=1":
				for li in data_list:
					company_url = "http://gcxm.hunanjs.gov.cn/AjaxHandler/PersonHandler.ashx?method=getCorpDetail&corpid={}&isout=".format(
						li.get("corpid"))
					yield Request(company_url, callback=self.parse_company, meta={"corpid": li.get("corpid"), "ty": ty})
			if ty == "type=5":
				for li in data_list:
					company_url = "http://gcxm.hunanjs.gov.cn/AjaxHandler/PersonHandler.ashx?method=getCorpDetail&corpid={}&isout=1".format(
						li.get("corpid"))
					yield Request(company_url, callback=self.parse_company, meta={"corpid": li.get("corpid"), "ty": ty})
		else:
			yield Request(response.url,callback=self.parse_companylist,dont_filter=True)
	def parse_company(self,response):
		mark = json.loads(response.text).get("success")
		if mark:
			ty = response.meta.get("ty")
			data = json.loads(response.text).get("data")
			ds_list = data.get("ds")
			if ty =="type=1":
				for ds in ds_list:
					hunan = HunanItem()
					hunan["id"] = response.meta.get("corpid")
					hunan["name"] = ds.get("corpname")
					hunan["social_credit_code"] = ds.get("corpcode")
					hunan["leal_person"] = ds.get("legalman")
					hunan["regis_type"] = ds.get("econtypename")
					hunan["reg_address"] = ds.get("county")
					hunan["address"] = ds.get("address")
					hunan["url"] = response.url
					hunan["create_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
					hunan["modification_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
					hunan["is_delete"] = 0
					ds1_list = data.get("ds1")
					if ds1_list:
						for ds1 in ds1_list:
							hunan["aptitude_type"] = ds1.get("aptitudekindname")
							hunan["aptitude_num"] = ds1.get("certid")
							hunan["aptitude_range"] = ds1.get("mark")
							hunan["aptitude_accept_date"] = ds1.get("organdate")
							if hunan["aptitude_accept_date"]:
								hunan["aptitude_accept_date"] = hunan["aptitude_accept_date"].strip("T00:00:00")
							hunan["aptitude_useful_date"] = ds1.get("enddate")
							if hunan["aptitude_useful_date"]:
								hunan["aptitude_useful_date"] = hunan["aptitude_useful_date"].strip("T00:00:00")
							hunan["aptitude_organ"] = ds1.get("organname")
							yield hunan
					else:
						yield hunan
			if ty =="type=5":
				for ds in ds_list:
					beian = BeianItem()
					beian["corpname"] = ds.get("corpname")
					beian["corpcode"] = ds.get("corpcode")
					beian["legalman"] = ds.get("legalman")
					beian["danweitype"] = ds.get("econtypename")
					beian["areaname"] = ds.get("county")
					beian["address"] = ds.get("address")
					beian["record_province"] = "湖南"
					beian["create_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
					beian["modification_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
					beian["is_delete"] = 0
					yield beian
		else:
			yield Request(response.url, callback=self.parse_company, dont_filter=True)



		



