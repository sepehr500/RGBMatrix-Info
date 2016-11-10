from bs4 import BeautifulSoup
import urllib2
import urllib
from pytrends.request import TrendReq
import json
import praw
from xml.dom import minidom
import xml.etree.ElementTree
import ConfigParser

class NewsInfo:
    configParser = ConfigParser.RawConfigParser()   
    configFilePath = 'Config.ini'
    configParser.readfp(open(configFilePath))
    RUser = configParser.get('News' ,'RUser') 
    RPass = configParser.get('News' ,'RPass') 
    GEmail= configParser.get('News' ,'GEmail') 
    GPass= configParser.get('News' ,'GPass') 
    @classmethod
    def GetRecentEventsReddit(self):
        pNounList = []
        newsList = []
        r = praw.Reddit(user_agent='Test Script by sep')
        r.login(self.RUser, self.RPass)
        submissions = r.get_subreddit('politics').get_top_from_hour(limit=5)
        submissions1 = r.get_subreddit('qualitynews').get_new(limit=10)
        submissions = list(submissions) + list(submissions1)
        for sub in submissions:
            print sub.title
            sub.title = sub.title.replace(u"\u2018", "'").replace(u"\u2019", "'")
            print(sub.title)
            s = " "
            if(len(sub.title.split())> 13):
              
              splitHead = sub.title.split()[:13]
              newTitle = s.join(splitHead) + "..."
            else:
              newTitle = sub.title
            newsList.append(newTitle)
            # for property, value in vars(sub).iteritems():
            #     print property, ": ", value
         
            
            

        return newsList
    #Also returns pictures
    @classmethod
    def GetRecentEventsGoogleTrends(self):
        print("trend call made")
        i = 0
        trendList  = []
        google_username = self.GEmail
        google_password = self.GPass
        path = ""
        pytrend = TrendReq(google_username, google_password, custom_useragent='My Pytrends Script')
        country_payload = {'geo': 'US' , 'date': 'today 1-H', 'cat':785 }
        # hottrends detail for pics
        hottrends = pytrend.hottrendsdetail(country_payload)
        # print(hottrends['1'])
        hottrends = hottrends.replace("ht:", "")
        xmldoc = xml.etree.ElementTree.fromstring(hottrends.encode('utf-8'))
        print(hottrends)
        #list of trending searches
        for x in xmldoc.findall(".//item/title"):
            print(x.text)
            trendList.append(x.text)
        #list of picture urls and download them
        # for x in xmldoc.findall(".//item/picture"):
        #     print(x.text)
        #     urllib.urlretrieve("http:"+x.text, str(i)+".jpg")
        #     i = i +1
        #description
        for x in xmldoc.findall(".//item/description"):
            #print(x.text)
            x = 6
            
        return trendList
        
            
        
    