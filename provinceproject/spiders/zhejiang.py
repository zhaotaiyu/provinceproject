# -*- coding: utf-8 -*-

from scrapy import Request,FormRequest
from provinceproject.items import *
import datetime
import re

class ZhejiangSpider(scrapy.Spider):
	name = 'zhejiang'
	#allowed_domains = ['115.29.2.37:8080/enterprise.php']
	start_urls = ['http://223.4.65.131:8080/enterprise_ajax.php']
	def parse(self, response):
		tr_list=response.xpath("//table[@class='t1']/tr[@class='auto_h']")
		for tr in tr_list:
			company_url=tr.xpath("./td[2]/div/a/@href").extract_first()
			msg = tr.xpath("./td[4]/div/text()").extract_first()
			if company_url:
				company_url="http://223.4.65.131:8080/"+company_url
				#company_url="http://223.4.65.131:8080/enterprise_detail.php?CORPCODE=68293005-2&SCUCode=91330106682930052T"
				yield Request(company_url,callback=self.parse_company,meta={"msg":msg,"dont_redirect":True})
		total_page=int(response.xpath("//span[@class='vcountPage']/text()").extract_first())
		now_page = int(response.xpath("//span[@class='vpage']/text()").extract_first())
		if now_page<=total_page:
			alt = response.xpath("//div[@id='pagebar']/ul/li[3]/@alt").extract_first()
			formdata={
				'page': alt
			}
			yield FormRequest(response.url,formdata=formdata,callback=self.parse)


	def parse_company(self,response):
		#http://115.29.2.37:8080/enterprise_detail.php?CORPCODE=56605492-1&SCUCode=91330105566054921P 无资质
		zhejiang = ZhejiangItem()
		zhejiang["id"] = response.url.split("=")[-1]
		zhejiang["name"] = response.xpath("//div[@class='detail_list']/table/tr[1]/td[2]/text()").extract_first()
		zhejiang["leal_person"] = response.xpath("//div[@class='detail_list']/table/tr[3]/td[2]/text()").extract_first()
		zhejiang["regis_type"] = response.xpath("//div[@class='detail_list']/table/tr[6]/td[2]/text()").extract_first()
		zhejiang["contact_person"] = response.xpath("//div[@class='detail_list']/table/tr[7]/td[2]/text()").extract_first()
		zhejiang["contact_address"] = response.xpath("//div[@class='detail_list']/table/tr[8]/td[2]/text()").extract_first()
		zhejiang["registered_capital"] = str(response.xpath("//div[@class='detail_list']/table/tr[2]/td[4]/text()").extract_first()).strip("欧美日万元(人民币) ").replace(" ","")
		zhejiang["leal_person_title"] = response.xpath("//div[@class='detail_list']/table/tr[3]/td[4]/text()").extract_first()
		zhejiang["build_date"] = str(response.xpath("//div[@class='detail_list']/table/tr[6]/td[4]/text()").extract_first()).strip(" -")
		gro=re.match("^(((?:19|20)\d\d)-(0?[1-9]|1[0-2])-(0?[1-9]|[12][0-9]|3[01]))$",zhejiang["build_date"])
		if gro is not None:
			zhejiang["build_date"] = gro.group(1)
		else:
			zhejiang["build_date"] = None
		zhejiang["reg_address_province"] = response.xpath("//div[@class='detail_list']/table/tr[7]/td[4]/text()").extract_first()
		zhejiang["social_credit_code"] = response.xpath("//div[@class='detail_list']/table/tr[2]/td[6]/text()").extract_first()
		if zhejiang["social_credit_code"] is None:
			zhejiang["social_credit_code"]=response.xpath("//div[@class='detail_list']/table/tr[2]/td[2]/text()").extract_first()
		zhejiang["leal_person_duty"]=response.xpath("//div[@class='detail_list']/table/tr[3]/td[6]/text()").extract_first()
		zhejiang["postalcode"]=response.xpath("//div[@class='detail_list']/table/tr[6]/td[6]/text()").extract_first()
		zhejiang["reg_address_city"]=response.xpath("//div[@class='detail_list']/table/tr[7]/td[6]/text()").extract_first()
		zhejiang["url"] = response.url
		zhejiang["create_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		zhejiang["modification_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		zhejiang["is_delete"] = 0
		if (response.meta.get("msg")).isspace() is False:
			aptitude_url = "http://223.4.65.131:8080//ajax_.php?page=1&"+response.url.split("?")[-1]
			yield Request(aptitude_url,callback=self.parse_aptitude,meta={"zhejiang":zhejiang,"dont_redirect":True})
		else:
			yield zhejiang
	def parse_aptitude(self,response):
		zhejiang = response.meta.get("zhejiang")
		div_list =response.xpath("//div[@class='zizhi']")
		if div_list:
			for div in div_list:
				zizhi_title = div.xpath("./div[@class='zizhi_title']/text()").extract_first().strip()
				if zizhi_title == "安全生产许可":
					if len(div_list) == 1:
						yield zhejiang
				else:
					zhejiang["aptitude_num"] = div.xpath("./div[@class='zizhi_list']/table/tr[1]/td[2]/text()").extract_first()
					zhejiang["aptitude_organ"] = div.xpath("./div[@class='zizhi_list']/table/tr[1]/td[4]/text()").extract_first()
					zhejiang["aptitude_accept_date"] = div.xpath("./div[@class='zizhi_list']/table/tr[2]/td[2]/text()").extract_first()
					if zhejiang["aptitude_accept_date"]:
						zhejiang["aptitude_accept_date"] =zhejiang["aptitude_accept_date"].replace("年","-").replace("月","-").strip(" -日")
					zhejiang["aptitude_useful_date"] = div.xpath("./div[@class='zizhi_list']/table/tr[2]/td[4]/text()").extract_first()
					if zhejiang["aptitude_useful_date"]:
						zhejiang["aptitude_useful_date"] = zhejiang["aptitude_useful_date"].replace("年","-").replace("月","-").strip(" -日")
					tr_list = div.xpath("./div[@class='zizhi_list']/table/tr[3]/td[2]/table/tr")
					for tr in tr_list[1::]:
						zhejiang["aptitude_range"] = tr.xpath("./td[1]/text()").extract_first()
						yield zhejiang
		else:
			yield zhejiang
