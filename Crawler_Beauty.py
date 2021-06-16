import os
import time
import requests
import shutil
import datetime
from collections import Counter
from bs4 import BeautifulSoup
from dateutil.parser import parse

def getRequest(url, fun_stream):
    while(1):
        try:
            r = requests.get(url, stream=fun_stream)
            break
        except:
            print("-----------------------------sleep")
            time.sleep(10)
    return r

def generateFile(folderName):
    path = './'+folderName
    try:
        os.mkdir(path)
        print("generate file success")
    except:
        print(folderName, "file exist")
    return path

def getArticle(dayBegin, dayEnd, laud):
    flag, page, meetArticle = 1, 1, []
    while(flag):
        if page == 1 : url = "https://www.pttweb.cc/bbs/Beauty/page"
        else : url = nextURL
        r = getRequest(url, False)
        soup = BeautifulSoup(r.text, "html.parser")
        articleSet = soup.find_all('div', class_='e7-container')
        for i in range(len(articleSet)):
            try:
                pushScore = articleSet[i].find_all('div', class_='e7-recommendScore')[0].text
                date = articleSet[i].find_all('span', class_='text-no-wrap')[1].text[:-6]
                if int(pushScore)>=laud and dayBegin<=parse(date)<=dayEnd:
                    meetArticle.append(articleSet[i].find('div', class_='e7-right-top-container').find('a').get('href'))
                elif dayBegin>parse(date):
                    flag=0
                    break
            except:
                pass
        nextURL = 'https://www.pttweb.cc'+soup.find_all('a', string='下一頁')[0].get('href')
        page += 1
    return meetArticle

def saveImage(article, folder):
    for page in article:
        url = 'https://www.pttweb.cc'+page
        r = getRequest(url, False)
        soup = BeautifulSoup(r.text, "html.parser")
        content = soup.find_all('a', class_='externalHref')[:-1]
        title = soup.find('span', itemprop='headline').text
        title.index('[')
        title = title[25:]
        for i in range(len(content)):
            imageURL = content[i].get('href')
            if 'https://i.imgur' in imageURL:
                r = getRequest(imageURL, True)
                imageName = folder+'\\'+title+'_'+str(i)+'.jpg'
                with open(imageName, 'wb+') as out_file:
                    shutil.copyfileobj(r.raw, out_file)

if __name__=='__main__':
    _folderName = "your_file_name"
    _dayBegin, _dayEnd, _laud = parse("2021-06-14"), parse("2021-06-15"), 30
    _folder = generateFile(_folderName)
    _article = getArticle(_dayBegin, _dayEnd, _laud)
    saveImage(_article, _folder)
