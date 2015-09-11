# -*- coding:utf-8 -*-
'''
Created on 2015年9月11日

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
import ThreadPool as threadPool


reload(sys)
#http://www.pythoner.com/200.html
#运行时没问题， 但是编译有有错误提示， 可以忽略。  
sys.setdefaultencoding('utf8')

class RGCRequestParser(object):
    
    def __init__(self):
        # uri = "mongodb://superuser:123456@host/?authSource=admin"
	#self.uri = "mongodb://superuser:123456@host/?authSource=admin"

        self.uri = "mongodb://superuser:123456@host/?authSource=admin"
        
        # slave
        # uri = "mongodb://superuser:123456@host/?authSource=admin"
        self.client = MongoClient(self.uri)
        self.db = self.client[u'rgconehour']
        self.posts = self.db.rgconehour
        # client = MongoClient('172.22.164.85')
        # result = client.the_database.authenticate('one', '12345', mechanism='SCRAM-SHA-1')
        # print(result)
        self.post = {"author": "Mike",
                    "text": "My first blog post!",
                    "tags": ["mongodb", "python", "pymongo"],
                    "date": datetime.datetime.utcnow()}
        self.__logger = mlogger
        self.__logger.__name__ = 'LBS log analyser'
        self.threadsize = 16
        self.tp = threadPool.ThreadPool(self.threadsize)
        
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
            try:
                #urls = self.htmlparser.parse_url(urlQueue.pop(), output_directory, target_url, crawl_interval, crawl_timeout)
                #self.tp.add_job(self.__anslyseAndStoreSingle, line, geocoder, rgc)
                self.__anslyseAndStoreSingle(line, geocoder, rgc)
            except Exception as ex:
                self.__logger.logerror(str(ex))
                self.__logger.logerror(line)
#             self.__anslyseAndStoreSingle(line, geocoder, rgc)
#             if (count % self.threadsize) == 0:
#                 self.tp.wait_for_complete()
            
    def __anslyseAndStoreSingle(self,line, geocoder,rgc):
        print('in thread')
        if "/geocoder/v2/" in line:
            #here deal with the web api request.
            try:
                bson = geocoder.getJson(line)
                
                print(bson)
                if bson is None:
                    return
                
                post_id = self.posts.insert_one(bson).inserted_id
            except Exception as e:
                self.__logger.logerror(str(e))
        elif "qt=rgc" in line:
            #here deal with the qt=rgc request.
            try:
                json = rgc.getJson(line)
                if json is None:
                    return
                print(json)
                post_id = self.posts.insert_one(json).inserted_id
            except Exception as e:
                self.__logger.logerror(str(e))
        else:
            #other types such as qt=rgc_stand
            print()
        
        
    def analyzelogfolder(self, folder):
        geocoder = Geocoder()
        rgc = RGC()
        for root, dirs, files in os.walk(folder):
            for f in files:
                filename = root + os.sep + f
                file_read = open(filename, 'r')
                # lines = file_read.readlines()
                for line in file_read:
                    try:
                    #urls = self.htmlparser.parse_url(urlQueue.pop(), output_directory, target_url, crawl_interval, crawl_timeout)
                    #self.tp.add_job(self.__anslyseAndStoreSingle, line, geocoder, rgc)
                        self.__anslyseAndStoreSingle(line, geocoder, rgc)
                    except Exception as ex:
                        self.__logger.logerror(str(ex))
                        self.__logger.logerror(line)
#             self.__anslyseAndStoreSingle(line, geocoder, rgc)
#             if (count % self.threadsize) == 0:
#                 self.tp.wait_for_complete()
                    #self.__analyseAndStore(lines)
                file_read.close()
                lines = []
                time.sleep(10)
            #self.__logger.loginfo()     


if __name__ == '__main__':
    analyser = RGCRequestParser()
    analyser.analyzelogfolder('/home/users/wanhao01/disk0/logs/loghz')
    #analyser.analyzelogfolder('Z:\\logs')
    #analyser.analyzelog('D:\\document\\ftp\\lighttpd.log.2015032315')
    #analyser.analyzelog('Z:\\logs\\lighttpd.log.2015032315')
    url = '112.239.176.138 112.239.176.138 3915248971 [23/Aug/2015:04:00:03 +0800] 17 "GET /geocoder/v2/?ak=VoljgjEANLKhKBIkvZiBt5GB&callback=renderReverse&location=36.851154,115.709744&output=json&pois=1&coordtype=wgs84ll HTTP/1.1" "api.map.baidu.com" 200 3162 gzip:100pct. "-" "-" "Apache-HttpClient/UNAVAILABLE (java 1.4)" map apimap 17183664298839117779 10.46.234.23 "10030602827970113114"' 
    print('-------------------------------------------------------------------------------------------------------------------------------')
    #analyser.testDB()
#     c = Geocoder()
#     print(c.getJson(url))
    pass
