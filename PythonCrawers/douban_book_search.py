__author__ = 'Maxiee'
# -*- coding: UTF-8 -*-

import mechanize
from bs4 import BeautifulSoup
import time

'''
程序功能：
    给出书名
    查询豆瓣图书，并返回相关信息
'''

BOOKNAME = 'CSS那些事儿'

URL = 'http://book.douban.com/subject_search?start=0&search_text='+ BOOKNAME

br = mechanize.Browser()
br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.addheaders = [('User-agent',
                  'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

response = br.open(URL)
soup = BeautifulSoup(response)
soup = soup.find('ul','subject-list')
count = 1

for tag in soup.find_all('li','subject-item'):
    info = tag.find('div','info')
    print u'%2d.书名：'%count +info.h2.a.get('title')
    print u'   连接：'+ tag.find('a','nbg').get('href')
    print u'   信息：'+ info.find('div','pub').get_text().strip()
    if tag.find('span','pl'):
        print u'   评价数：'+ tag.find('span','pl').get_text().strip()
    if tag.find('span','rating_nums'):
        print u'   评分：'+ tag.find('span','rating_nums').get_text()
    count += 1
