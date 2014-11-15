__author__ = 'maxiee'

import urllib.request
import re
from bs4 import BeautifulSoup

def crawl(url):
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page)
    for tag in soup.find_all('div','item'):
        m_order = int(tag.find('em').get_text())
        m_name = tag.find('span','title').get_text()
        m_rating_score = tag.find('div','star').find('em').get_text()
        print("%s %s %s" % (m_order, m_name, m_rating_score))

if __name__ == '__main__':
    print('豆瓣电影TOP250:\n')
    for i in range(10):
        base = i * 25
        crawl('http://movie.douban.com/top250?start=%d' % (base))
