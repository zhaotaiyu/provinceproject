# -*- coding: utf-8 -*-

from scrapy import Request,FormRequest
from provinceproject.items import *
import datetime
import re

class ZhejiangSpider(scrapy.Spider):
	name = 'zhejiang'
	custom_settings = {
		'DOWNLOAD_DELAY': '0.1',
		# 'DOWNLOADER_MIDDLEWARES' : {'provinceproject.middlewares.AbuyunProxyMiddleware': 543}
	}
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
		c_info = CompanyInfomortation()
		c_info["province_company_id"] = response.url.split("=")[-1]
		c_info["company_name"] = response.xpath("//div[@class='detail_list']/table/tr[1]/td[2]/text()").extract_first()
		c_info["leal_person"] = response.xpath("//div[@class='detail_list']/table/tr[3]/td[2]/text()").extract_first()
		c_info["regis_type"] = response.xpath("//div[@class='detail_list']/table/tr[6]/td[2]/text()").extract_first()
		c_info["contact_person"] = response.xpath("//div[@class='detail_list']/table/tr[7]/td[2]/text()").extract_first()
		c_info["contact_address"] = response.xpath("//div[@class='detail_list']/table/tr[8]/td[2]/text()").extract_first()
		c_info["registered_capital"] = str(response.xpath("//div[@class='detail_list']/table/tr[2]/td[4]/text()").extract_first()).strip("欧美日万元(人民币) ").replace(" ","")
		c_info["leal_person_title"] = response.xpath("//div[@class='detail_list']/table/tr[3]/td[4]/text()").extract_first()
		c_info["build_date"] = str(response.xpath("//div[@class='detail_list']/table/tr[6]/td[4]/text()").extract_first()).strip(" -")
		gro=re.match("^(((?:19|20)\d\d)-(0?[1-9]|1[0-2])-(0?[1-9]|[12][0-9]|3[01]))$",c_info["build_date"])
		if gro is not None:
			c_info["build_date"] = gro.group(1)
		else:
			c_info["build_date"] = None
		c_info["regis_address"] = str(response.xpath("//div[@class='detail_list']/table/tr[7]/td[4]/text()").extract_first()).strip() + "-" + str(response.xpath("//div[@class='detail_list']/table/tr[7]/td[6]/text()").extract_first()).strip()
		c_info["social_credit_code"] = response.xpath("//div[@class='detail_list']/table/tr[2]/td[6]/text()").extract_first()
		if c_info["social_credit_code"] is None:
			c_info["social_credit_code"]=response.xpath("//div[@class='detail_list']/table/tr[2]/td[2]/text()").extract_first()
		c_info["leal_person_duty"]=response.xpath("//div[@class='detail_list']/table/tr[3]/td[6]/text()").extract_first()
		c_info["postalcode"]=response.xpath("//div[@class='detail_list']/table/tr[6]/td[6]/text()").extract_first()
		c_info["url"] = response.url
		c_info["source"] = "浙江"
		yield c_info
		if (response.meta.get("msg")).isspace() is False:
			aptitude_url = "http://223.4.65.131:8080//ajax_.php?page=1&"+response.url.split("?")[-1]
			yield Request(aptitude_url,callback=self.parse_aptitude,meta={"province_company_id":c_info["province_company_id"],"company_name":c_info["company_name"],"dont_redirect":True})
	def parse_aptitude(self,response):
		div_list =response.xpath("//div[@class='zizhi']")
		if div_list:
			for div in div_list:
				zizhi_title = div.xpath("./div[@class='zizhi_title']/text()").extract_first().strip()
				if zizhi_title == "安全生产许可":
					pass
					# if len(div_list) == 1:
				else:
					c_apt = CompanyaptitudeItem()
					c_apt["province_company_id"] = response.meta.get("province_company_id")
					c_apt["company_name"] = response.meta.get("company_name")
					c_apt["source"] = "浙江"
					c_apt["aptitude_id"] = div.xpath("./div[@class='zizhi_list']/table/tr[1]/td[2]/text()").extract_first()
					c_apt["aptitude_organ"] = div.xpath("./div[@class='zizhi_list']/table/tr[1]/td[4]/text()").extract_first()
					c_apt["aptitude_startime"] = div.xpath("./div[@class='zizhi_list']/table/tr[2]/td[2]/text()").extract_first()
					if c_apt["aptitude_startime"]:
						c_apt["aptitude_startime"] =c_apt["aptitude_startime"].replace("年","-").replace("月","-").strip(" -日")
					c_apt["aptitude_endtime"] = div.xpath("./div[@class='zizhi_list']/table/tr[2]/td[4]/text()").extract_first()
					if c_apt["aptitude_endtime"]:
						c_apt["aptitude_endtime"] = c_apt["aptitude_endtime"].replace("年","-").replace("月","-").strip(" -日")
					tr_list = div.xpath("./div[@class='zizhi_list']/table/tr[3]/td[2]/table/tr")
					for tr in tr_list[1::]:
						c_apt["aptitude_name"] = tr.xpath("./td[1]/text()").extract_first()
						yield c_apt
