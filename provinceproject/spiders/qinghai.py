# -*- coding: utf-8 -*-
import datetime
import re
from scrapy import FormRequest, Request
from provinceproject.items import *

class QinghaiSpider(scrapy.Spider):
    name = 'qinghai'
    custom_settings = {
        'DOWNLOAD_DELAY': '0.1',
        #'DOWNLOADER_MIDDLEWARES': {'provinceproject.middlewares.AbuyunProxyMiddleware': 543, }
    }
    allowed_domains = ['139.170.150.135']
    start_urls = ['http://139.170.150.135/dataservice/query/comp/list/SW','http://139.170.150.135/dataservice/query/comp/list/BS']

    def parse(self, response):
        # total_page = dict(response.xpath("//a[@sf='pagebar']/@*[name()='sf:data']").extract_first().strip("()")).get("pc")
        total_page = int(re.findall(".*?pc:(\d+).*", response.xpath("//a[@sf='pagebar']/@*[name()='sf:data']").extract_first())[0])
        for page in range(1, total_page + 1):
            # for page in range(1, 50):
            formdata = {
                '$total': str(total_page),
                '$reload': '0',
                '$pg': str(page),
                '$pgsz': '15'
            }
            yield FormRequest(response.url, formdata=formdata, callback=self.parse_companylist)

    def parse_companylist(self, response):
        mark = response.url.split("/")[-1]
        tr_list = response.xpath("//table[@class='table_box']/tbody/tr")
        for tr in tr_list:
            company_url = "http://139.170.150.135" + tr.xpath("./@onclick").extract_first().split("'")[1]
            yield Request(company_url, callback=self.parse_company, meta={"mark": mark})

    def parse_company(self, response):
        if response.meta.get("mark") == "BS":
            c_info = CompanyInfomortation()
            province_company_id = "qinghai_" + response.url.split("/")[-1]
            c_info["province_company_id"] = province_company_id
            c_info["company_name"] = response.xpath("//span[@class='user-name']/text()").extract_first()
            c_info["social_credit_code"] = response.xpath("//div[@class='bottom']/dl[1]/dt/text()").extract_first()
            if c_info["social_credit_code"] is None:
                c_info["social_credit_code"] = response.xpath("//div[@class='bottom']/dl[1]/dd/text()").extract_first()
            c_info["leal_person"] = response.xpath("//div[@class='bottom']/dl[2]/dd/text()").extract_first()
            c_info["regis_type"] = response.xpath("//div[@class='bottom']/dl[3]/dd/text()").extract_first()
            c_info["build_date"] = "-".join(re.findall("\d+", str(response.xpath("//div[@class='bottom']/dl[3]/dt/text()").extract_first())))
            c_info["regis_address"] = response.xpath("//div[@class='bottom']/dl[4]/dd/text()").extract_first()
            c_info["business_address"] = response.xpath("//div[@class='bottom']/dl[5]/dd/text()").extract_first()
            c_info["url"] = response.url
            c_info["area_code"] = "630000"
            c_info["source"] = "青海"
            yield c_info
            aptitude_url = "http://139.170.150.135/dataservice/query/comp/caDetailList/{}".format(
                province_company_id)
            yield Request(aptitude_url, callback=self.parse_companyaptitude,meta={"province_company_id": province_company_id,"company_name": c_info["company_name"]})
        else:
            beian = BeianItem()
            beian["social_credit_code"] = response.xpath("//div[@class='bottom']/dl[1]/dt/text()").extract_first()
            beian["company_name"] = response.xpath("//span[@class='user-name']/text()").extract_first()
            beian["record_province"] = "青海"
            yield beian

    def parse_companyaptitude(self, response):
        tr_list = response.xpath("//table[@class='pro_table_box tableMerged']/tbody/tr[@class='row']")
        if tr_list:
            for tr in tr_list:
                c_apt = CompanyaptitudeItem()
                c_apt["company_name"] = response.meta.get("company_name")
                c_apt["province_company_id"] = response.meta.get("province_company_id")
                c_apt["aptitude_name"] = str(tr.xpath("./td[2]/text()").extract_first()).strip()
                c_apt["aptitude_startime"] = tr.xpath("./td[3]/text()").extract_first()
                c_apt["aptitude_id"] = tr.xpath("./td[4]/text()").extract_first()
                c_apt["aptitude_organ"] = tr.xpath("./td[5]/text()").extract_first()
                yield c_apt