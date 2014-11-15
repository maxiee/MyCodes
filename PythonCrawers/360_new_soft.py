__author__ = 'maxiee'

import mechanize
from bs4 import BeautifulSoup

br = mechanize.Browser()

for page in range(10):
    print(page)
    url = "http://zhushou.360.cn/list/index/cid/1/order/newest?page="+str(page)
    response = br.open(url)
    # print(response.read())
    soup = BeautifulSoup(response)
    soup = soup.find('ul','iconList')
    # print(soup)
    url_base = 'http://zhushou.360.cn'
    for tag in soup.find_all('li'):
        print(tag.h3.get_text() + '\t' + url_base + tag.a.get('href'))


