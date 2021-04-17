from bs4 import BeautifulSoup as soup
import requests
import datetime
import os
import time

yesterday = datetime.date.today() - datetime.timedelta(days = 1)
cnn_url = 'https://www.cnn.com/business'
cnn_path = '/home/andrerg01/AutoTraders/DataBase/HTML/CNN_Business'

run = False
yesterday = datetime.date.today() - datetime.timedelta(days = 1)
while True:
    if run:
        print("Checking for CNN Business headlines from " + str(yesterday))
        html = requests.get(cnn_url)
        bsobj = soup(html.content)
        
        articleURLs = []
        for news in bsobj.findAll('h3'):
            tempURL = news.a.get('href')
            if tempURL.startswith('/' + str(yesterday.year) + '/' + str(yesterday.month).zfill(2) + '/' + str(yesterday.day).zfill(2)):
                articleURLs += ['https://www.cnn.com' + news.a.get('href')]
        
        print(str(len(articleURLs)) + " article(s) found.")
        print("Saving articles to database.")
        
        i = 0
        for article in articleURLs:
            articleHTML = requests.get(article)
            articleBS = soup(articleHTML.content)
            os.system('mkdir ' + cnn_path + '/' + str(yesterday))
            with open(cnn_path + '/' + str(yesterday) + '/' + str(i).zfill(2) + '.html', 'w') as f:
                f.write(str(articleBS))
            i += 1
        
        print("Files saved! Sleeping now till tomorrow")
        
        yesterday = datetime.date.today() - datetime.timedelta(days = 1)
        run = False
    else:
        if (datetime.date.today() - datetime.timedelta(days = 1)).day != yesterday.day:
            run = True
        else:
            time.sleep(60*60)
            