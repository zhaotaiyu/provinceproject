# -*- coding: utf-8 -*-
import logging
import requests
import json,time
import random,datetime

orderid = '966404044351881'  # 订单号
# 提取代理链接，以私密代理为例
api_url = "http://dps.kdlapi.com/api/getdps/?orderid={}&num=1&pt=1&f_et=1&format=json&sep=1"
headers = {
    "Accept-Encoding": "Gzip",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
}
def fetch_one_proxy():
    logging.debug("**********************************切换代理*********************************************")
    time.sleep(1)
    while 1:
        time.sleep(2)
        fetch_url = api_url.format(orderid)
        r = requests.get(fetch_url,timeout=5)
        if r.status_code == 200:
            content = json.loads(r.content.decode('utf-8'))
            print(content)
            ips = content['data']['proxy_list']
            proxy =ips[0].split(",")[0]
            use_time = int(ips[0].split(",")[1])
            get_time = int(time.time())
            return proxy,use_time,get_time


