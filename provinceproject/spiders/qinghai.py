# -*- coding: utf-8 -*-
import datetime
import re
import scrapy
from scrapy import FormRequest, Request
from provinceproject.items import *


class QinghaiSpider(scrapy.Spider):
    name = 'qinghai'
    allowed_domains = ['139.170.150.135']
    start_urls = ['http://139.170.150.135/dataservice/query/comp/list/BS/']

    def parse(self, response):
        if response.url == 'http://139.170.150.135/dataservice/query/comp/list/BS/':
            total_page = int(re.findall('.*?\$total":(\d+)',response.xpath("//div[@class='clearfix']/script/text()").extract_first())[0])
            # for page in range(1,total_page):
            for page in range(1, 3):
                formdata = {
                    '$total':str(total_page),
                    '$reload':'0',
                    '$pg':str(page),
                    '$pgsz':'15'
                }
                yield FormRequest(response.url,formdata=formdata,callback=self.parse_companylist)
    def parse_companylist(self,response):
        tr_list = response.xpath("//table[@class='table_box']/tbody/tr")
        for tr in tr_list:
            company_url = "http://139.170.150.135" + tr.xpath("./@onclick").extract_first().split("'")[1]
            yield Request(company_url,callback=self.parse_company)
    def parse_company(self,response):
        qinghai = QinghaiItem()
        company_id = response.url.split("/")[-1]
        qinghai["id"] = company_id
        qinghai["name"] = response.xpath("//span[@class='user-name']/text()").extract_first()
        qinghai["social_credit_code"] = response.xpath("//div[@class='bottom']/dl[1]/dt/text()").extract_first()
        if qinghai["social_credit_code"] is None:
            qinghai["social_credit_code"] = response.xpath("//div[@class='bottom']/dl[1]/dd/text()").extract_first()
        qinghai["leal_person"] = response.xpath("//div[@class='bottom']/dl[2]/dd/text()").extract_first()
        qinghai["regis_type"] = response.xpath("//div[@class='bottom']/dl[3]/dd/text()").extract_first()
        qinghai["build_date"] = response.xpath("//div[@class='bottom']/dl[3]/dt/text()").extract_first()
        qinghai["reg_address"] = response.xpath("//div[@class='bottom']/dl[4]/dd/text()").extract_first()
        qinghai["address"] = response.xpath("//div[@class='bottom']/dl[5]/dd/text()").extract_first()
        qinghai["url"] = response.url
        qinghai["create_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        qinghai["modification_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        qinghai["is_delete"] = 0
        aptitude_url = "http://139.170.150.135/dataservice/query/comp/caDetailList/{}".format(company_id)
        yield Request(aptitude_url,callback=self.parse_companyaptitude,meta={"qinghai":qinghai})
    def parse_companyaptitude(self,response):
        qinghai = response.meta.get("qinghai")
        tr_list = response.xpath("//table[@class='pro_table_box tableMerged']/tbody/tr[@class='row']")
        if tr_list:
            for tr in tr_list:
                qinghai["aptitude_type"] = str(tr.xpath("./td[2]/text()").extract_first()).strip()
                qinghai["aptitude_accept_date"] = tr.xpath("./td[3]/text()").extract_first()
                qinghai["aptitude_num"] = tr.xpath("./td[4]/text()").extract_first()
                qinghai["aptitude_organ"] = tr.xpath("./td[5]/text()").extract_first()
                yield qinghai
        else:
            yield qinghai

