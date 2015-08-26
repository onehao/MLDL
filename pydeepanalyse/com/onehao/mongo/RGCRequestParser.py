# -*- coding:utf-8 -*-
'''
Created on 2015年8月26日

@author: wanhao01
'''
import datetime
import httplib, urllib
import json
import os
import random
import sys
import time

from bson.objectid import ObjectId
import pymongo
from pymongo.mongo_client import MongoClient

from com.onehao import mlogger
from com.onehao.mongo.RgcStructure import Geocoder, RGC


reload(sys)
#http://www.pythoner.com/200.html
#运行时没问题， 但是编译有有错误提示， 可以忽略。  
sys.setdefaultencoding('utf8')

class RGCRequestParser(object):
    
    def __init__(self):
        # uri = "mongodb://superuser:123456@172.22.164.85/?authSource=admin"
        # master
        self.uri = "mongodb://superuser:123456@10.95.103.66:8801/?authSource=admin"
        
        # slave
        # uri = "mongodb://superuser:123456@220.181.3.211/?authSource=admin"
        self.client = MongoClient(self.uri)
        self.db = self.client[u'rgctest']
        self.posts = self.db.posts
        # client = MongoClient('172.22.164.85')
        # result = client.the_database.authenticate('one', '12345', mechanism='SCRAM-SHA-1')
        # print(result)
        self.post = {"author": "Mike",
                    "text": "My first blog post!",
                    "tags": ["mongodb", "python", "pymongo"],
                    "date": datetime.datetime.utcnow()}
        self.__logger = mlogger
        self.__logger.__name__ = 'LBS log analyser'
        
    def get(self,post_id):
        document = self.posts.find_one({'_id':ObjectId(post_id)})
        print(document)
    
    def testDB(self):
        
        print self.client.database_names()
        
#         post_id = self.posts.insert_one(self.post).inserted_id
#         print(post_id)
#         print self.posts.find_one()
#         self.get(post_id)
        for p in self.posts.find():
            print(p)
    def __analyseAndStore(self, lines):
        geocoder = Geocoder()
        rgc = RGC()
        for line in lines:
            if "/geocoder/v2/" in line:
                #here deal with the web api request.
                try:
                    bson = geocoder.getJson(line)
                    if bson is None:
                        continue
                    print(bson)
                    post_id = self.posts.insert_one(bson).inserted_id
                except Exception as e:
                    self.__logger.logerror(str(e))
            elif "qt=rgc" in line:
                #here deal with the qt=rgc request.
                try:
                    json = rgc.getJson(line)
                    if json is None:
                        continue
                    print(json)
                    post_id = self.posts.insert_one(json).inserted_id
                except Exception as e:
                    self.__logger.logerror(str(e))
            else:
                #other types such as qt=rgc_stand
                print()
        
        
    def analyzelogfolder(self, folder):
            for root, dirs, files in os.walk(folder):
                for f in files:
                    filename = root + os.sep + f
                    file_read = open(filename, 'r')
                    lines = file_read.readlines()
                    self.__analyseAndStore(lines)
                    file_read.close()
                    lines = []
                    time.sleep(10)
            #self.__logger.loginfo()     


if __name__ == '__main__':
    analyser = RGCRequestParser()
#     analyser.analyzelogfolder('D:\\logs')
    #analyser.analyzelogfolder('Z:\\logs')
    #analyser.analyzelog('D:\\document\\ftp\\lighttpd.log.2015032315')
    #analyser.analyzelog('Z:\\logs\\lighttpd.log.2015032315')
    url = '112.239.176.138 112.239.176.138 3915248971 [23/Aug/2015:04:00:03 +0800] 17 "GET /geocoder/v2/?ak=VoljgjEANLKhKBIkvZiBt5GB&callback=renderReverse&location=36.851154,115.709744&output=json&pois=1&coordtype=wgs84ll HTTP/1.1" "api.map.baidu.com" 200 3162 gzip:100pct. "-" "-" "Apache-HttpClient/UNAVAILABLE (java 1.4)" map apimap 17183664298839117779 10.46.234.23 "10030602827970113114"' 
    print('-------------------------------------------------------------------------------------------------------------------------------')
    analyser.testDB()
#     c = Geocoder()
#     print(c.getJson(url))
    pass