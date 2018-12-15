import requests 
from urllib.parse import urlencode
#from selenium import webdriver
from pyquery import PyQuery as pq 
import time 
import pymysql
import sys 
import re
import os

ulrlist = ['http://www.wzwood.com/video/30.html','http://www.wzwood.com/video/31.html','http://www.wzwood.com/video/31/2.html','http://www.wzwood.com/video/52/2.html','http://www.wzwood.com/video/52/3.html','http://www.wzwood.com/video/52/4.html','http://www.wzwood.com/video/52.html',]
def getall(url):
    req = requests.get(url)
    #print(req.text)
    return req.text
def killpb (result):
    p_url = re.compile('/video/show-\d*'+'.html')
    p_m3u8_1 = re.compile('vMp4url = "'+'\S*'+'.m3u8')
    p_m3u8_2 = re.compile('video: \''+'\S*'+'.m3u8')
    doc = pq (result)
    title_all = doc('li').items()
    for i  in title_all:
        try:
            title = i.find('h2')
            title = str(title).replace('</h2>&#13;','')
            title = title.replace('<h2>','')
            title = title.replace(' ','')
            title_result = title.replace('\n','')
            print(title_result)
            i = str(i)
            url = re.search(p_url,i).group(0)
            url = 'http://www.wzwood.com'+url
            head = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}
            m3u8 = requests.get(url,headers = head)
            m3u8 = m3u8.text
        
        


            m3u8_result_1 = re.search(p_m3u8_1,m3u8).group(0)
            m3u8_result_2 = re.search(p_m3u8_2,m3u8).group(0)
            
            m3u8_result_1 = m3u8_result_1.replace('vMp4url = "','')
            m3u8_result_2 = m3u8_result_2.replace('video: \'','')
            m3u8_result_1 = 'http://www.wzwood.com'+m3u8_result_1
            print(m3u8_result_1)
            print(m3u8_result_2)
            status_m3u8_1 = requests.get(m3u8_result_1,timeout = 3)
            status_m3u8_2 = requests.get(m3u8_result_2,timeout = 3)
            print(status_m3u8_1.status_code,status_m3u8_2.status_code)
            if (status_m3u8_1.status_code == 200 and status_m3u8_2.status_code == 200):
                num_1 = status_m3u8_1.text.count('.ts')
                print(num_1)
                num_2 = status_m3u8_2.text.count('.ts')
                print(num_2)
                if (num_1>num_2):
                    m3u8_result = m3u8_result_1
                elif (num_2 > num_1):
                    m3u8_result = m3u8_result_2
                elif (num_1 == num_2):
                    m3u8_result = m3u8_result_1 = m3u8_result_2
            
            elif(status_m3u8_1.status_code != 200 and status_m3u8_2.status_code != 200):
                continue
            
            elif (status_m3u8_1.status_code == 200 and status_m3u8_2.status_code != 200):
                m3u8_result = m3u8_result_1

            elif (status_m3u8_1.status_code != 200 and status_m3u8_2.status_code == 200):
                m3u8_result = m3u8_result_2

            status_result = 100
            db = pymysql.connect(host = 'XXXXX',user = 'XXXX',password = 'XXXXX',port = 3306,db = 'XXXXXXX',charset = 'utf8')
            cursor = db.cursor()
            sql = 'INSERT INTO fantastic(name,adrees,ST) values(%s,%s,%s) ON DUPLICATE KEY UPDATE name = %s ,adrees = %s ,ST = %s  '
            try:
                cursor.execute(sql,(title_result,m3u8_result,status_result)*2)
                db.commit()
                print ('successful!')
            except:
                db.rollback()
        except:
            continue
            
for i in ulrlist:        
    print(i)
    result = getall(i)
    killpb (result)


