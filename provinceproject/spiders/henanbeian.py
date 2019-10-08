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
		total_page = int(response.xpath("//div[@id='AspNetPager2']/ul/li[13]/a/text()").extract_first()) +1
		__VIEWSTATE = response.xpath("//input[@id='__VIEWSTATE']/@value").extract_first()
		__EVENTVALIDATION = response.xpath("//input[@id='__EVENTVALIDATION']/@value").extract_first()
		__VIEWSTATEGENERATOR = response.xpath("//input[@id='__VIEWSTATEGENERATOR']/@value").extract_first()
		for page in range(10,total_page):
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
		for tr in tr_list[1:-1]:
			beian = BeianItem()
			beian["social_credit_code"] = tr.xpath("./td[2]/a/@href").extract_first().split("=")[-1]
			beian["company_name"] = tr.xpath("./td[2]/a/@href").extract_first().split("=")[-2].split("&")[0]
			beian["record_province"] = "河南"
			yield beian

	

