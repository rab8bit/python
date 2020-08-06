#!/usr/bin/env python3
import requests
import datetime
from bs4 import BeautifulSoup
#from pathlib import Path

months = {'января':1,'февраля':2,'марта':3,'апреля':4,'мая':5,'июня':6,'июля':7,'августа':8,'сентября':9,'октября':10,'ноября':11,'декабря':12}
key_words=['О плановых работах по обслуживанию оборудования ВетИС','Об очередном обновлении','ВетИС','О нагрузочных испытаниях']
current_date = [str(datetime.datetime.now().day) ,str(datetime.datetime.now().month) , str(datetime.datetime.now().year) ]

url="http://vetrf.ru/vetrf/news"
head = {
"user-agent":
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
"Content-Type":
"application/x-www-form-urlencoded; charset=UTF-8"
}
current_news = []
def find_new(new_div):
    nws_link = new_div.find('h4').find('a').get('href')
    nws_desc = new_div.find('h4').find('a').text
    nws_date = new_div.find('span',{'class':'conn-date'}).text.split()
    nws_date = [nws_date[0], str(months[nws_date[1]]),nws_date[2]]
    return nws_link,nws_desc,nws_date

def maching_news(nws_lst):
    for news in nws_lst:
        news_link,news_desc,news_date = find_new(news)
        if current_date == news_date :
            
            if any( key_word in news_desc for key_word in key_words):
                current_news.append([news_desc,'http://vetrf.ru'+news_link])
            
    return current_news

response=requests.get(url,head)
soup = BeautifulSoup(response.text,"lxml")
news_list = soup.find_all('div',{'class':'conn-post'})

curnews = maching_news(news_list)

try:
  f = open("/tmp/check_merkury_news.dat","r+")
  nnews = len(curnews) - int(f.read())
  for n in curnews[0:nnews]:
    print(*n, sep='\n')
  f.seek(0)
  f.write(str(len(curnews)))
except:
  f = open("/tmp/check_merkury_news.dat","w")
  for n in curnews:
    print(*n, sep='\n')
  f.write(str(len(curnews)))
finally:
  f.close()
