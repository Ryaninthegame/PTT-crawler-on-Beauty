import os
import time
import requests
import shutil
import datetime
from collections import Counter
from bs4 import BeautifulSoup
from dateutil.parser import parse

def get_r(fun_url, fun_stream):
    while(1):
        try:
            fun_r=requests.get(fun_url, stream=fun_stream)
            break
        except:
            print('********sleep********')
            time.sleep(10)
    return fun_r

def generate_file(fun_name):
    file_name='./'+fun_name
    try:
        os.mkdir(file_name)
        print('generate file success')
    except:
        print(file_name, 'file exist')
    return file_name

def get_page(fun_day_begin, fun_day_end, fun_laud):
    flag, page, page_list = 1, 1, []
    while(flag):
        if page==1:url='https://www.pttweb.cc/bbs/beauty/page'
        else:url=next_url
        r=get_r(url, False)
        soup=BeautifulSoup(r.text, "html.parser")
        article_list=soup.find_all('div', class_='e7-container')
        for index in range(len(article_list)):
            try:
                push=article_list[index].find_all('div', class_='e7-recommendScore')[0].text
                time_=article_list[index].find_all('span', class_='text-no-wrap')[1].text[:-6]
                if int(push)>=fun_laud and fun_day_begin<=parse(time_)<=fun_day_end:
                    page_list.append(article_list[index].find('div', class_='e7-right-top-container').find('a').get('href'))
                elif fun_day_begin>parse(time_):
                    flag=0
                    break
            except:
                pass
        next_url='https://www.pttweb.cc'+soup.find_all('a', string='下一頁')[0].get('href')
        page+=1
    return page_list

def save_image(fun_page_list, fun_file_name):
    for page in fun_page_list:
        url='https://www.pttweb.cc'+page
        r=get_r(url, False)
        soup=BeautifulSoup(r.text, "html.parser")
        content=soup.find_all('a', class_='externalHref')[:-1]
        title=soup.find('span', itemprop='headline').text
        title.index('[')
        title=title[25:]
        for item_index in range(len(content)):
            img_url=content[item_index].get('href')
            if 'https://i.imgur' in img_url:
                r=get_r(img_url, True)
                img_name=fun_file_name+'\\'+title+'_'+str(item_index)+'.jpg'
                with open(img_name, 'wb+') as out_file:
                    shutil.copyfileobj(r.raw, out_file)

if __name__=='__main__':
    file_name='your_file_name'
    day_begin, day_end, laud = parse("2021-02-24"), parse("2021-02-25"), 30
    file_=generate_file(file_name)
    list_=get_page(day_begin, day_end, laud)
    save_image(list_, file_)