# -*- coding: utf-8 -*-
import scrapy
from scrapy import FormRequest,Request

class GansuSpider(scrapy.Spider):
    name = 'gansu'
    #allowed_domains = ['61.178.32.163:84/GSJZJGweb/index.aspx?tabid=1f1e1aa9-6feb-40ed-a063-6f8a27d9ed04']
    start_urls = ['http://61.178.32.163:84/GSJZJGweb/index.aspx?tabid=1f1e1aa9-6feb-40ed-a063-6f8a27d9ed04']

    def parse(self, response):
        url="http://61.178.32.163:84/GSJZJGweb/index.aspx?tabid=1f1e1aa9-6feb-40ed-a063-6f8a27d9ed04"
        __VIEWSTATE=response.xpath("//input[@id='__VIEWSTATE']/@value").extract_first()
        __VIEWSTATEGENERATOR=response.xpath("//input[@id='__VIEWSTATEGENERATOR']/@value").extract_first()
        __EVENTVALIDATION=response.xpath("//input[@id='__EVENTVALIDATION']/@value").extract_first()
   #      formdata={
   #      	'Webb_Upload_Enable': 'False',
			# '__VIEWSTATE':__VIEWSTATE,
			# '__VIEWSTATEGENERATOR':__VIEWSTATEGENERATOR,
			# '__EVENTVALIDATION':__EVENTVALIDATION,
			# 'keyword':'站内搜索',
   #      }
        formdata={
        	'Webb_Upload_Enable':'False',
			'__EVENTTARGET':'',
			'__EVENTARGUMENT':'',
			'__LASTFOCUS':'',
			'__VIEWSTATE':'HQH3hn0tQMUenkQrfZeqYD4QWC0Wd%2BfheRVmGU5FFjH6x2nkLE783AzDGXNIbhrvhHz6CkRz88dPxBlfs8ZyAoA88A1FQuGA3MWAnPf0X89lzVQiUZsyIct%2BR2Fk8PAouuKtUScS0tLgg5QooMWoj3BF5QE1PxccEUZ2fcm3ocPDHlJTxzykKo18TsduULHgNOiBksb%2FAWuAW4i%2Fn7o%2FINbtdZ3JSs5YxMKhGRJT4BepZteJ%2B0ukZdg%2FroET61bJX%2Bwjyq0jvDGDaVSo%2FXfa6wA3oNzwCBbVV%2F5qWwWmTYBojC0ms%2ByL00MVAU3esxJ2qvy64%2BHQT2MnDzTtDwhKefCEfq%2FRVyiaEXfn5XNi8aY7UxMDj7MaQldcGcsaja48mvF2gGyGBj7bUitbhriwzwDXUiar3cKtnAYnJ%2FyJQMyzCbpgF%2BpcoVvftHUZqlA4DAv2OvtILXmVF2CKZ3yXLCkjzjvaJkanRjgwOyc9SEIpqjXwATnrR7GcRNfjMpUAKts5uOY1QO%2BjTMwVfwSrwpiTv3YAANTLnV12TZuCWe2ZSZi7mzaKXgCnothZ5F8D4h817kaT9RsHfQsIvPTQvY49kgLKm3osRpjpERaNjUJuVKvEEMtMv2C9hRXt2%2FFKKA%2FHDycsC4fVCFu5cm7bxYPZkpuzq7DG8eifCHST89fCFxcbWU5ccnqdyTJdSJRQEtIbtdY1PYkdT%2BQewHmcYAsHu1BKxFmNQjDBxTCI0Im0qiJmfo9%2BaVWiXhnNIsTlveCgT5YBrAQHkmoGBqjAyfA%2BV8aA1FXVr54OpuGM8R4M7UaQGGDNIa8G1lk5ncmRHLdfvzCpoHE8%2FdNw%2Fb894OAyXUBQy6QdIvEfIWfDLxDXk78LaVWZnvIDZu0nzp7waljxEPHPWVFOV0tilNC%2FYWD6ikzpSj893yStsn4UC3nwKkIl2u5OkX7FWBBPoEZ4DngMHFXJQzKxJYO9%2BgrEO17JFIHjuLSV7WuFlEbKYtPU6UyzeeL9iSRUqRSbM%2FSY3TGVoNyEDiurqSIbtKTywn9AbGWO35F0tqzhz5m2SICi1XZrnI5WvKCmx7oiyhSrxlW2iA%3D%3D',
			'__VIEWSTATEGENERATOR':'6AA129B5',
			'__VIEWSTATEENCRYPTED':'',
			'__EVENTVALIDATION':'WylkHrW5L0FpG%2BwJL6clBIKS7%2Fz4TGUPL2Kp8GtmA09%2BGHp3a5Ap2xy77bQjf%2B%2Bbh8Bu8M9zjiwTjk19AWSY7qb7XODLXJE4y9B6XkqAv7FgnCNmMZH637gYeqC%2FEavdPFJLMNhhkAOTDTvffEdF1vm8e0hHQgCPG0EbUlfE5bNaRmC3dTz4rdEZ%2F0%2FBVXAZSZn1hRLsFZTR2p1iEKQnn9ga7YW64%2BrUl89oAhDUI6xSc6caf6nYBUIorx0LRlKTvBKfXz2YRDQ2Qon2KWxV33d2maO8c8k046A1AZN25KRswNcg',
			'keyword':'%E7%AB%99%E5%86%85%E6%90%9C%E7%B4%A2',
			'_ctl10%3AtbEnterpriseName':'',
			'_ctl10%3AdprlRegionCode':'',
			'_ctl10%3AdropAptitudeType':'',
			'_ctl10%3AtxtAptitudeName':'',
			'_ctl10%3AbtnDemand':'',
        }

        print(formdata)
        yield FormRequest(url,formdata=formdata,callback=self.parse_company_list)
    def parse_company_list(self,response):
    	print(response.text)
