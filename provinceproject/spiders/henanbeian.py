# -*- coding: utf-8 -*-
import scrapy,datetime
from scrapy import Request,FormRequest
from provinceproject.items import *

class HenanbeianSpider(scrapy.Spider):
	name = 'henanbeian'
	#allowed_domains = ['hngcjs.hnjs.gov.cn/SiKuWeb/WSRY_List.aspx']
	start_urls = ['http://hngcjs.hnjs.gov.cn/SiKuWeb/WSRY_List.aspx']

	def parse(self, response):
		now_page = int(response.xpath("//div[@id='AspNetPager2']/ul/li//span[@class='active']/text()").extract_first())
		total_page = int(response.xpath("//div[@id='AspNetPager2']/ul/li[13]/a/text()").extract_first())
		__VIEWSTATE = response.xpath("//input[@id='__VIEWSTATE']/@value").extract_first()
		__EVENTVALIDATION = response.xpath("//input[@id='__EVENTVALIDATION']/@value").extract_first()
		__VIEWSTATEGENERATOR = response.xpath("//input[@id='__VIEWSTATEGENERATOR']/@value").extract_first()
		for page in range(2,3):
			formdata = {
				'__EVENTTARGET':'AspNetPager2',
				'__EVENTARGUMENT':str(page),
				'__VIEWSTATE':__VIEWSTATE,
				'__VIEWSTATEGENERATOR':__VIEWSTATEGENERATOR,
				'__EVENTVALIDATION':__EVENTVALIDATION,
			}
			yield FormRequest(response.url,formdata=formdata,callback=self.parse_companylist)
	def parse_companylist(self,response):
		tr_list = response.xpath("//table[@id='ContentPlaceHolder1_GridView2']/tbody/tr")
		for tr in tr_list[2:]:
			corpname = tr.xpath("./td[2]/a/text()").extract_first()
			corpcode = tr.xpath("./td[3]/text()").extract_first()
			company_url = "http://hngcjs.hnjs.gov.cn/SiKuWeb/WSRY_Detail.aspx?QiYeMingCheng={}&TongYiSheHuiXinYongDaiMa={}".format(corpname,corpcode)
			if corpcode:
				yield Request(company_url,callback=self.parse_company,meta={"CorpCode":corpcode,"CorpName":corpname})
			else:
				print(corpname)
				print(corpcode)
				stop = input("===============")

	def parse_company(self,response):
		beian = BeianItem()
		beian["corpcode"] = response.meta.get("CorpCode")
		beian ["corpname"] = response.meta.get("CorpName")
		beian["areaname"] = str(response.xpath("//table[@class='Tab']/tr[4]/td[2]/span/text()").extract_first()).strip()
		beian["regprin"] = str(response.xpath("//table[@class='Tab']/tr[4]/td[4]/span/text()").extract_first()).strip()
		beian["legalman"] = str(response.xpath("//table[@class='Tab']/tr[3]/td[2]/span/text()").extract_first()).strip()
		beian["economicnum"] = str(response.xpath("//table[@class='Tab']/tr[3]/td[4]/span/text()").extract_first()).strip()
		beian["address"] = str(response.xpath("//table[@class='Tab']/tr[5]/td[2]/span/text()").extract_first()).strip()
		beian["record_province"] = "河南"
		beian["create_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		beian["modification_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		beian["is_delete"] = 0
		yield beian
	

