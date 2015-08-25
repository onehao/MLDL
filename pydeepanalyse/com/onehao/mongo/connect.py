#coding=utf-8  
'''
@author: Michael Wan
@since: 2015-08-25
'''
import httplib, urllib
import json
import random
import sys

import pymongo
from pymongo.mongo_client import MongoClient


reload(sys)
#http://www.pythoner.com/200.html
#运行时没问题， 但是编译有有错误提示， 可以忽略。  
sys.setdefaultencoding('utf8')

uri = "mongodb://superuser:123456@172.22.164.85/?authSource=admin"
client = MongoClient(uri)
print(client.database_names())
# client = MongoClient('172.22.164.85')
# result = client.the_database.authenticate('one', '12345', mechanism='SCRAM-SHA-1')
# print(result)