# -*- coding:utf-8 -*-
'''
Created on 2015.8.26

@author: wanhao01
'''
import json
import re

from com.onehao import mlogger


class Geocoder:
    """class for Geocoder/v2""" 
    ak = ""
    coordtype = ""
    lng = ""
    lat = ""
    time = ""
    type=""
    pattern = ""
    #112.239.176.138 112.239.176.138 3915248971 [23/Aug/2015:04:00:03 +0800] 17 "GET /geocoder/v2/?ak=VoljgjEANLKhKBIkvZiBt5GB&callback=renderReverse&location=36.851154,115.709744&output=json&pois=1&coordtype=wgs84ll HTTP/1.1" "api.jsonmap.baidu.com" 200 3162 gzip:100pct. "-" "-" "Apache-HttpClient/UNAVAILABLE (java 1.4)" jsonmap apimap 17183664298839117779 10.46.234.23 "10030602827970113114" 
    
    def __init__(self):
        self.coordtype = "wgs84ll" 
        self.type = "geocoder"
        self.pattern="/geocoder/v2"
        self.__logger = mlogger
        self.__logger.__name__ = 'LBS log analyser'
        
    def getJson(self, line):
        jsonmap = dict()
        try:
            # Get time.
            patternTime = re.compile('\[.*?\]',re.DOTALL)
            matchTime = patternTime.findall(line)
            if len(matchTime) > 0: 
                time =  matchTime[0][1:-1]
            else:
                return
            # Parsing parameters
            pattern = re.compile('\"GET ' + self.pattern + '.*?HTTP/1.1\"',re.DOTALL)
            match = pattern.findall(line)
            parameters = ''
            if len(match) > 0: 
                parameters =  match[0]
                start = parameters.index('?') + 1
                end = parameters.index('HTTP') - 1
                parameters = parameters[start:end]
            else:
                return    
            parameterList = parameters.split('&')
            from cStringIO import StringIO
#             file_str = StringIO()
            jsonmap['type'] = 'geocoderv2'
            jsonmap['time'] = time
#             file_str.write('\"type\":\"geocoderv2\",')
#             file_str.write('\"time\":\"' + time + '\",') 
            for parameter in parameterList:
                keyvalue = parameter.split('=')
                if keyvalue[0] == 'location':
                    latlng=keyvalue[1].split(',')
                    lat = latlng[0]
                    lng = latlng[1]
                    jsonmap['lat'] = lat
                    jsonmap['lng'] = lng
#                     file_str.write('\"lat\":\"' + lat + '\",') 
#                     file_str.write('\"lng\":\"' + lng + '\",')   
                else:
                    jsonmap[keyvalue[0]] = keyvalue[1]
#                     file_str.write('\"' + keyvalue[0] + '\":\"' + keyvalue[1] + '\",')
            return jsonmap
        except Exception as e:
            self.__logger.logerror(str(e))

    
class RGC:
    """class for qt=rgc"""  
    ak = ""
    type=""
    Coordinate_type=""
    im=""
    Imsi=""
    Os=""
    Prod=""
    Resid=""
    Oem=""
    Channcel=""
    Cuid=""
    Uid=""
    Screen=""
    Dpi=""
    Ver=""
    Ctm=""
    Pcn=""
    Bt=""
    Extf=""
    Mb=""


    def __init__(self): 
        self.coordtype = "wgs84ll" 
        self.type = "rgc"
        
    def getJson(self,line):
        jsonmap = dict()
        try:
            # Get time.
            patternTime = re.compile('\[.*?\]',re.DOTALL)
            matchTime = patternTime.findall(line)
            if len(matchTime) > 0: 
                time =  matchTime[0][1:-1]
            else:
                return ''
            # Parsing parameters
            pattern = re.compile('\"GET .*?HTTP/1.1\"',re.DOTALL)
            match = pattern.findall(line)
            parameters = ''
            if len(match) > 0: 
                parameters =  match[0]
                start = parameters.index('?') + 1
                end = parameters.index('HTTP') - 1
                parameters = parameters[start:end]
            else:
                return ''    
            parameterList = parameters.split('&')
            from cStringIO import StringIO
            file_str = StringIO()
#             file_str.write('{')
            jsonmap['type'] = 'geocoderv2'
            jsonmap['time'] = time
#             file_str.write('\"type\":\"rgc\",') 
#             file_str.write('\"time\":\"' + time + '\",') 
            for parameter in parameterList:
                keyvalue = parameter.split('=')
                if keyvalue[0] == 'x':
                    jsonmap['lng'] = keyvalue[1]
#                     file_str.write('\"lng\":\"' + keyvalue[1] + '\",') 
                elif keyvalue[0] == 'y':
                    jsonmap['lat'] = keyvalue[1]
#                     file_str.write('\"lat\":\"' + keyvalue[1] + '\",') 
                else:
                    jsonmap[keyvalue[0]] = keyvalue[1]
#                     file_str.write('\"' + keyvalue[0] + '\":\"' + keyvalue[1] + '\",')
#             file_str.write('}')
            
            return jsonmap
        except Exception as e:
            self.__logger.logerror(str(e)) 

        
class RGCStand:
    """class for qt=rgc_stand"""  
    ak = ""
    type=""
    coordtype = ""
    lng = ""
    lat = ""
    time = ""

    def __init__(self): 
        self.coordtype = "wgs84ll" 
        self.type="rgc_stand"
        
    def getJson(self):
        from cStringIO import StringIO

        file_str = StringIO()
        
        file_str.write('{\"ak\":\"' + self.ak + '\",')
        file_str.write('\"akcoordtype\":\"' + self.coordtype + '\",')
        file_str.write('\"lng\":\"' + self.lng + '\",')
        file_str.write('\"lat\":\"' + self.lat + '\",')
        file_str.write('\"time\":\"' + self.time + '\"}')
        
        return file_str.getvalue()
        
