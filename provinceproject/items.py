# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import scrapy

class ProvinceprojectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
#备案
class BeianItem(scrapy.Item):
    #collection="beian"
    collection="beian_copy1"
    corpcode = scrapy.Field()
    corpname = scrapy.Field()
    danweitype = scrapy.Field()
    areacode = scrapy.Field()
    areaname = scrapy.Field()
    certcode = scrapy.Field()
    validdate = scrapy.Field()
    qualificationscope = scrapy.Field()
    regprin = scrapy.Field()
    legalman = scrapy.Field()
    legalmanprotitle = scrapy.Field()
    legalmanduty = scrapy.Field()
    economicnum = scrapy.Field()
    corpbirthdate = scrapy.Field()
    postalcode = scrapy.Field()
    linkman = scrapy.Field()
    linktel = scrapy.Field()
    fax = scrapy.Field()
    address = scrapy.Field()
    titlelevelnum = scrapy.Field()
    record_province = scrapy.Field()
    create_time = scrapy.Field()
    modification_time = scrapy.Field()
    is_delete = scrapy.Field()
#湖北
class HubeiItem(scrapy.Item):
    collection="hubei"
    id = scrapy.Field()
    name = scrapy.Field()
    reg_address = scrapy.Field()
    social_credit_code = scrapy.Field()
    regis_type = scrapy.Field()
    leal_person = scrapy.Field()
    leal_person_duty = scrapy.Field()
    tech_lead = scrapy.Field()
    tech_lead_duty = scrapy.Field()
    anistrative_lic_num = scrapy.Field()
    lic_start_date = scrapy.Field()
    lic_organ = scrapy.Field()
    remark = scrapy.Field()
    registered_capital = scrapy.Field()
    build_date = scrapy.Field()
    leal_person_title = scrapy.Field()
    technicalleader_title = scrapy.Field()
    lic_num = scrapy.Field()
    lic_useful_date = scrapy.Field()
    lic_indate = scrapy.Field()
    lic_name = scrapy.Field()
    url = scrapy.Field()
    create_time = scrapy.Field()
    modification_time = scrapy.Field()
    is_delete = scrapy.Field()
#江西
class JiangxiItem(scrapy.Item):
    collection = "jiangxi"
    id= scrapy.Field()
    name= scrapy.Field()
    leal_person= scrapy.Field()
    address= scrapy.Field()
    social_credit_code= scrapy.Field()
    regis_type= scrapy.Field()
    registered_capital= scrapy.Field()
    lic_num= scrapy.Field()
    lic_useful_date= scrapy.Field()
    lic_organ= scrapy.Field()
    aptitude_level= scrapy.Field()
    aptitude_type= scrapy.Field()
    check_time= scrapy.Field()
    url= scrapy.Field()
    create_time= scrapy.Field()
    modification_time= scrapy.Field()
    is_delete= scrapy.Field()
#山东
class ShandongItem(scrapy.Item):
    collection="shandong"
    show = scrapy.Field()
    timestamp = scrapy.Field()
    certid = scrapy.Field()
    organname = scrapy.Field()
    organdate = scrapy.Field()
    ceoname = scrapy.Field()
    ctoname = scrapy.Field()
    enddate = scrapy.Field()
    qualificationscope = scrapy.Field()
    corpcode = scrapy.Field()
    corpname = scrapy.Field()
    sourceouname = scrapy.Field()
    create_time = scrapy.Field()
    modification_time = scrapy.Field()
    is_delete = scrapy.Field()
#陕西
class Shanxi3Item(scrapy.Item):
    collection="shanxi3"
    id = scrapy.Field()
    name = scrapy.Field()
    lic_accept_date = scrapy.Field()
    aptitude_type = scrapy.Field()
    social_credit_code = scrapy.Field()
    reg_address = scrapy.Field()
    lic_num = scrapy.Field()
    lic_useful_date = scrapy.Field()
    leal_person = scrapy.Field()
    url = scrapy.Field()
    create_time = scrapy.Field()
    modification_time = scrapy.Field()
    is_delete = scrapy.Field()
#广东
class GuangdongItem(scrapy.Item):
    collection="guangdong"
    id = scrapy.Field()
    name = scrapy.Field()
    lic_accept_date = scrapy.Field()
    aptitude_type = scrapy.Field()
    social_credit_code = scrapy.Field()
    reg_address = scrapy.Field()
    lic_num = scrapy.Field()
    lic_useful_date = scrapy.Field()
    leal_person = scrapy.Field()
    url = scrapy.Field()
    create_time = scrapy.Field()
    modification_time = scrapy.Field()
    is_delete = scrapy.Field()
#广西
class GuangxiItem(scrapy.Item):
    collection="guangxi"
    id = scrapy.Field()
    name = scrapy.Field()
    leal_person = scrapy.Field()
    build_date = scrapy.Field()
    contact_person = scrapy.Field()
    lic_num = scrapy.Field()
    reg_address = scrapy.Field()
    remark = scrapy.Field()
    registered_capital = scrapy.Field()
    leal_person_title = scrapy.Field()
    postalcode = scrapy.Field()
    contact_phone = scrapy.Field()
    contact_address = scrapy.Field()
    social_credit_code = scrapy.Field()
    tech_lead_duty = scrapy.Field()
    fax = scrapy.Field()
    aptitude_num = scrapy.Field()
    aptitude_organ = scrapy.Field()
    aptitude_accept_date = scrapy.Field()
    aptitude_useful_date = scrapy.Field()
    aptitude_type = scrapy.Field()
    aptitude_range = scrapy.Field()
    url = scrapy.Field()
    create_time = scrapy.Field()
    modification_time = scrapy.Field()
    is_delete = scrapy.Field()
#辽宁
class LiaoningItem(scrapy.Item):
    collection="liaoning"
    id=scrapy.Field()
    name=scrapy.Field()
    social_credit_code=scrapy.Field()
    leal_person=scrapy.Field()
    reg_address=scrapy.Field()
    remark=scrapy.Field()
    regis_type=scrapy.Field()
    contact_address=scrapy.Field()
    aptitude_num=scrapy.Field()
    aptitude_accept_date=scrapy.Field()
    aptitude_range=scrapy.Field()
    aptitude_organ=scrapy.Field()
    aptitude_useful_date=scrapy.Field()
    url=scrapy.Field()
    create_time=scrapy.Field()
    modification_time=scrapy.Field()
    is_delete=scrapy.Field()
#内蒙古
class NeimengguItem(scrapy.Item):
    collection="neimenggu"
    id = scrapy.Field()
    name = scrapy.Field()
    social_credit_code = scrapy.Field()
    leal_person = scrapy.Field()
    regis_type = scrapy.Field()
    contact_person = scrapy.Field()
    contact_address = scrapy.Field()
    registered_capital = scrapy.Field()
    leal_person_title = scrapy.Field()
    build_date = scrapy.Field()
    reg_address = scrapy.Field()
    tech_lead_duty = scrapy.Field()
    postalcode = scrapy.Field()
    reg_address_city = scrapy.Field()
    aptitude_num = scrapy.Field()
    aptitude_accept_date = scrapy.Field()
    aptitude_range = scrapy.Field()
    aptitude_organ = scrapy.Field()
    aptitude_useful_date = scrapy.Field()
    url = scrapy.Field()
    create_time = scrapy.Field()
    modification_time = scrapy.Field()
    is_delete = scrapy.Field()
    com_lead= scrapy.Field()
    tech_lead= scrapy.Field()
#宁夏
class NingxiaItem(scrapy.Item):
    collection="ningxia"
    id = scrapy.Field()
    name = scrapy.Field()
    reg_address = scrapy.Field()
    social_credit_code = scrapy.Field()
    registered_capital = scrapy.Field()
    leal_person = scrapy.Field()
    build_date = scrapy.Field()
    tel = scrapy.Field()
    fax = scrapy.Field()
    website = scrapy.Field()
    email = scrapy.Field()
    postalcode = scrapy.Field()
    reg_address_province = scrapy.Field()
    reg_address_city = scrapy.Field()
    reg_address_country = scrapy.Field()
    contact_person = scrapy.Field()
    contact_tel = scrapy.Field()
    contact_phone = scrapy.Field()
    aptitude_credit_score= scrapy.Field()
    aptitude_sequence= scrapy.Field()
    aptitude_credit_level= scrapy.Field()
    aptitude_speciality= scrapy.Field()
    aptitude_type= scrapy.Field()
    aptitude_level= scrapy.Field()
    create_time = scrapy.Field()
    modification_time = scrapy.Field()
    is_delete = scrapy.Field()
#新疆
class XinjiangItem(scrapy.Item):
    collection="xinjiang"
    id=scrapy.Field()
    name=scrapy.Field()
    social_credit_code=scrapy.Field()
    leal_person=scrapy.Field()
    regis_type=scrapy.Field()
    build_date=scrapy.Field()
    reg_address=scrapy.Field()
    address=scrapy.Field()
    aptitude_range=scrapy.Field()
    aptitude_accept_date=scrapy.Field()
    aptitude_num=scrapy.Field()
    aptitude_organ=scrapy.Field()
    url=scrapy.Field()
    create_time=scrapy.Field()
    modification_time=scrapy.Field()
    is_delete=scrapy.Field()
#西藏
class XizangItem(scrapy.Item):
    collection="xizang"
    id = scrapy.Field()
    name = scrapy.Field()
    leal_person = scrapy.Field()
    regis_type = scrapy.Field()
    contact_person = scrapy.Field()
    contact_address = scrapy.Field()
    registered_capital = scrapy.Field()
    leal_person_title = scrapy.Field()
    build_date = scrapy.Field()
    reg_address_province = scrapy.Field()
    social_credit_code = scrapy.Field()
    leal_person_duty = scrapy.Field()
    postalcode = scrapy.Field()
    reg_address_city = scrapy.Field()
    aptitude_num = scrapy.Field()
    aptitude_accept_date = scrapy.Field()
    aptitude_range = scrapy.Field()
    aptitude_organ = scrapy.Field()
    aptitude_useful_date = scrapy.Field()
    tech_lead = scrapy.Field()
    url = scrapy.Field()
    create_time = scrapy.Field()
    modification_time = scrapy.Field()
    is_delete = scrapy.Field()
#北京
class BeijingItem(scrapy.Item):
    collection="beijing"
    id = scrapy.Field()
    name = scrapy.Field()
    address = scrapy.Field()
    registered_capital = scrapy.Field()
    social_credit_code = scrapy.Field()
    regis_type = scrapy.Field()
    leal_person = scrapy.Field()
    aptitude_num = scrapy.Field()
    aptitude_range = scrapy.Field()
    aptitude_organ = scrapy.Field()
    aptitude_accept_date = scrapy.Field()
    aptitude_useful_date = scrapy.Field()
    url = scrapy.Field()
    create_time = scrapy.Field()
    modification_time = scrapy.Field()
    is_delete = scrapy.Field()
#浙江
class ZhejiangItem(scrapy.Item):
    collection = "zhejiang"
    id = scrapy.Field()
    name = scrapy.Field()
    leal_person = scrapy.Field()
    regis_type = scrapy.Field()
    contact_person = scrapy.Field()
    contact_address = scrapy.Field()
    registered_capital = scrapy.Field()
    leal_person_title = scrapy.Field()
    build_date = scrapy.Field()
    reg_address_province = scrapy.Field()
    social_credit_code = scrapy.Field()
    leal_person_duty = scrapy.Field()
    postalcode = scrapy.Field()
    reg_address_city = scrapy.Field()
    aptitude_num = scrapy.Field()
    aptitude_organ = scrapy.Field()
    aptitude_accept_date = scrapy.Field()
    aptitude_useful_date = scrapy.Field()
    aptitude_range = scrapy.Field()
    url = scrapy.Field()
    create_time = scrapy.Field()
    modification_time = scrapy.Field()
    is_delete = scrapy.Field()
#湖南
class HunanItem(scrapy.Item):
    collection = "hunan"
    id = scrapy.Field()
    name = scrapy.Field()
    social_credit_code = scrapy.Field()
    leal_person = scrapy.Field()
    regis_type = scrapy.Field()
    reg_address = scrapy.Field()
    address = scrapy.Field()
    url = scrapy.Field()
    aptitude_type = scrapy.Field()
    aptitude_num = scrapy.Field()
    aptitude_range = scrapy.Field()
    aptitude_accept_date = scrapy.Field()
    aptitude_useful_date = scrapy.Field()
    aptitude_organ = scrapy.Field()
    create_time = scrapy.Field()
    modification_time = scrapy.Field()
    is_delete = scrapy.Field()
#安徽
class AnhuiItem(scrapy.Item):
    collection = "anhui"
    id = scrapy.Field()
    name = scrapy.Field()
    social_credit_code = scrapy.Field()
    leal_person = scrapy.Field()
    regis_type = scrapy.Field()
    reg_address = scrapy.Field()
    address = scrapy.Field()
    url = scrapy.Field()
    aptitude_type = scrapy.Field()
    aptitude_num = scrapy.Field()
    aptitude_range = scrapy.Field()
    aptitude_useful_date = scrapy.Field()
    aptitude_organ = scrapy.Field()
    create_time = scrapy.Field()
    modification_time = scrapy.Field()
    is_delete = scrapy.Field()




