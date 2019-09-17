# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import datetime
import pymongo
import psycopg2
from .settings import *


class CeshiPipeline(object):
    def process_item(self, item, spider):
        print(item)
        return item
class ProvinceprojectPipeline(object):
    def process_item(self, item, spider):
        for key, value in item.items():
            if value is None:
                item[key] = "None"
        return item

class PgsqlPipeline(object):
    def __init__(self, pgsql_uri, pgsql_db,pgsql_user,pgsql_pass,pgsql_port):
        self.pgsql_uri = pgsql_uri
        self.pgsql_db = pgsql_db
        self.pgsql_user = pgsql_user
        self.pgsql_pass = pgsql_pass
        self.pgsql_port=pgsql_port
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            pgsql_uri=crawler.settings.get('PGSQL_URI'),
            pgsql_db=crawler.settings.get('PGSQL_DATABASE'),
            pgsql_user =crawler.settings.get('PGSQL_USER'),
            pgsql_pass=crawler.settings.get('PGSQL_PASS'),
            pgsql_port=crawler.settings.get('PGSQL_PORT')
        )

    def open_spider(self, spider):
        # 创建连接对象
        self.db = psycopg2.connect(database=self.pgsql_db, user=self.pgsql_user, password=self.pgsql_pass, host=self.pgsql_uri, port=self.pgsql_port)
        self.cursor = self.db.cursor()  # 创建指针对象
        print("已连接数据库")

    def close_spider(self, spider):
        # 关闭练级
        print("已关闭数据库")
        self.cursor.close()
        self.db.close()
    def process_item(self,item,spider):
        ite=dict(item)
        sql="INSERT INTO {} (".format(item.collection)
        v_list=[]
        k_list=[]
        for key,value in ite.items():
            if value !="None" and value !="":
                sql += "{},"
                v_list.append(ite[key])
                k_list.append(key)
        sql=sql.format(*k_list)[:-1]+")"+" VALUES ("
        for key,value in ite.items():
            if value !="None" and value !="":
                sql += "'{}',"
        sql=sql.format(*v_list)[:-1]+")"
        try:
            self.cursor.execute(sql)
            self.db.commit()
            print("写入一条")
        except Exception as e:
            self.db.rollback()
            try:
                self.db = psycopg2.connect(database=self.pgsql_db, user=self.pgsql_user, password=self.pgsql_pass,
                                           host=self.pgsql_uri, port=self.pgsql_port)
                self.cursor = self.db.cursor()
                self.cursor.execute(sql)
                self.db.commit()
            except:
                myclient = pymongo.MongoClient('mongodb://ecs-a025-0002:27017/')
                mydb = myclient[MONGODATABASE]
                mycol = mydb[MONGOTABLE]
                mydict = {"item": item, "reason": "写入数据库失败", 'sql': sql,
                          'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                mycol.insert_one(mydict)
                myclient.close()
        return item