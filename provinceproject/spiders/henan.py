# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request,FormRequest


class HenanSpider(scrapy.Spider):
	name = 'henan'
	#allowed_domains = ['hngcjs.hnjs.gov.cn/SiKuWeb/QiyeList.aspx?type=qyxx']
	start_urls = ['http://hngcjs.hnjs.gov.cn/SiKuWeb/QiyeList.aspx?type=qyxx']

	def parse(self, response):
		now_page = int(response.xpath("//div[@id='AspNetPager2']/ul/li//span[@class='active']/text()").extract_first())
		total_page = int(response.xpath("//div[@id='AspNetPager2']/ul/li[13]/a/text()").extract_first())
		if now_page < total_page:
			__VIEWSTATE = response.xpath("//input[@id='__VIEWSTATE']/@value").extract_first()
			__EVENTVALIDATION = response.xpath("//input[@id='__EVENTVALIDATION']/@value").extract_first()
			__VIEWSTATEGENERATOR = response.xpath("//input[@id='__VIEWSTATEGENERATOR']/@value").extract_first()
			formdata = {
				'__EVENTTARGET':'AspNetPager2',
				'__EVENTARGUMENT':str(now_page + 1),
				'__VIEWSTATE':__VIEWSTATE,
				'__VIEWSTATEGENERATOR':__VIEWSTATEGENERATOR,
				'__EVENTVALIDATION':__EVENTVALIDATION,
				'CretType':'全部企业类别',
			}
			yield FormRequest(response.url,formdata=formdata,callback=self.parse)
		tr_list = response.xpath("//div[@id='tagContenth0']/table/tbody/tr")
		for tr in tr_list[2:]:
			CorpName = tr.xpath("./td[2]/a/text()").extract_first()
			CorpCode = tr.xpath("./td[3]/text()").extract_first()
			company_url = "http://hngcjs.hnjs.gov.cn/SiKuWeb/QiyeDetail.aspx?CorpName={}&CorpCode={}".format(CorpName,CorpCode)
			yield Request(company_url,callback=self.parse_company,meta={""})

		
	def parse_company(self,response):
		print(response.url)
		id
		name
		reg_address
		build_date
		address
		leal_person
		contact_person
		social_credit_code
		regis_type
		postalcode
		tech_lead_duty
		website
		aptitude_type
		aptitude_num
		aptitude_accept_date
		aptitude_range
		aptitude_organ
		aptitude_useful_date
		url
		create_time
		modification_time
		is_delete

