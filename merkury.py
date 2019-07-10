#!/usr/bin/env python3
import requests
import datetime
from bs4 import BeautifulSoup

months = {'января':'1','февраля':'2','марта':'3','апреля':'4','мая':'5','июня':'6','июля':'7','августа':'8','сентября':'9','октября':'10','ноября':'11','декабря':'12'}
current_date = [datetime.datetime.now().day , datetime.datetime.now().month , datetime.datetime.now().year ]
#current_date = ['5','7','2019']
url="http://vetrf.ru/vetrf/news"
head = {
"user-agent": 
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
"Content-Type": 
"application/x-www-form-urlencoded; charset=UTF-8"
}
response=requests.get(url,head)
#print(response.text)
soup = BeautifulSoup(response.text,"lxml")
news_list = soup.find_all('div',{'class':'conn-post'})
#print("current date",current_date)
for news in news_list:
    news_link = news.find('h4').find('a').get('href')
    news_desc = news.find('h4').find('a').text
    news_date = news.find('span',{'class':'conn-date'}).text.split()
    news_date = [news_date[0], months[news_date[1]],news_date[2]]
 #   print(news_date)
    if current_date == news_date :
 #       print('news date',news_date)
        if "О плановых работах по обслуживанию оборудования ВетИС" in news_desc:
            print("Новость: {0} \n <a href={1}>подробнее</a>".format(news_desc,news_link)) 

#print(news_list)



