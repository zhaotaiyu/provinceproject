# -*- coding: utf-8 -*-
import scrapy


class GuangdongSpider(scrapy.Spider):
    name = 'guangdong'
    allowed_domains = ['113.108.219.40/Dop/Open/EnterpriseList.aspx']
    start_urls = ['http://113.108.219.40/Dop/Open/EnterpriseList.aspx/']

    def parse(self, response):
        pass


# guangdong["id"]=
# guangdong["name"]=
# guangdong["lic_accept_date"]=
# guangdong["aptitude_type"]=
# guangdong["social_credit_code"]=
# guangdong["reg_address"]=
# guangdong["lic_num"]=
# guangdong["lic_useful_date"]=
# guangdong["leal_person"]=
# guangdong["url"]=
# guangdong["create_time"]=
# guangdong["modification_time"]=
# guangdong["is_delete"]=
