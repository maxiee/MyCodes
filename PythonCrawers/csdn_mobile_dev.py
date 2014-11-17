__author__ = 'Maxiee'
# -*- coding: UTF-8 -*-

import mechanize
from bs4 import BeautifulSoup

'''
程序功能：查看CSDN博客移动开发分类
'''

#设置Python编码，否则不能创建文件
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# 浏览器伪装
br = mechanize.Browser()
br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.addheaders = [('User-agent',
                  'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

for page in range(1, 10):
    url = 'http://blog.csdn.net/mobile/index.html?&page=' + str(page)
    response = br.open(url)
    soup = BeautifulSoup(response)


    # file.write("正在加载第%d页:\r\n\r\n" % (page))
    print("正在加载第%d页:\n" % (page))

    for tag in soup.find_all('div', 'blog_list'):
        tag_h1 = tag.find('h1').find_all('a')
        if (len(tag_h1)) == 2:
            cat = tag_h1[0].get_text()
            title = tag_h1[1].get_text()
            url = tag_h1[1].get('href')
        else:
            title = tag_h1[0].get_text()
            cat = ''
            url = tag_h1[0].get('href')
        # file.write(u'\t标题:' + cat + title+u"\r\n")
        # file.write(u'\t链接: ' + url + u'\r\n\r\n')
        print(u'\t标题:' + cat + title)
        print(u'\t链接: ' + url+u'\n')

# file.close()
print("载入完成")
