__author__ = 'Maxiee'
# -*- coding: UTF-8 -*-

import mechanize
from bs4 import BeautifulSoup
import time

'''
程序功能：
    爬取Android开发咨询：EOE社区，CSDN
    生成一个HTML文档，调用浏览器打开
'''

# 设置Python编码，否则不能创建文件
import sys

reload(sys)
# for Linux/Unix
# sys.setdefaultencoding('utf-8')
# for Windows
sys.setdefaultencoding('gbk')


def eoe_crawer(br):
    base_url = 'http://www.eoeandroid.com/'
    sub_cat_url = (
        'http://www.eoeandroid.com/forum.php?mod=forumdisplay&fid=53&filter=lastpost&orderby=lastpost',
        'http://www.eoeandroid.com/forum.php?mod=forumdisplay&fid=93&filter=lastpost&orderby=lastpost',
        'http://www.eoeandroid.com/forum.php?mod=forumdisplay&fid=45&filter=lastpost&orderby=lastpost',
        'http://www.eoeandroid.com/forum.php?mod=forumdisplay&fid=27&filter=lastpost&orderby=lastpost',
        'http://www.eoeandroid.com/forum.php?mod=forumdisplay&fid=89&filter=lastpost&orderby=lastpost',
        'http://www.eoeandroid.com/forum.php?mod=forumdisplay&fid=23&filter=lastpost&orderby=lastpost',
        'http://www.eoeandroid.com/forum.php?mod=forumdisplay&fid=15&filter=lastpost&orderby=lastpost',
        'http://www.eoeandroid.com/forum.php?mod=forumdisplay&fid=208&filter=lastpost&orderby=lastpost',
        'http://www.eoeandroid.com/forum.php?mod=forumdisplay&fid=207&filter=lastpost&orderby=lastpost',
        'http://www.eoeandroid.com/forum.php?mod=forumdisplay&fid=200&filter=lastpost&orderby=lastpost',
        'http://www.eoeandroid.com/forum.php?mod=forumdisplay&fid=843&filter=lastpost&orderby=lastpost',
        'http://www.eoeandroid.com/forum.php?mod=forumdisplay&fid=182&filter=lastpost&orderby=lastpost',
        'http://www.eoeandroid.com/forum.php?mod=forumdisplay&fid=808&filter=lastpost&orderby=lastpost')
    sub_cat_name = (
        u"新手入门", u"经验分享", u"开发问答", u"实例教程", u"盈利模式", u"源码分享", u"资料分享", u"UI界面",
        u"开源项目", u"视频教程", u"电子图书", u"游戏开发", u"Cocos2D")
    length = len(sub_cat_name)
    data = []
    for i in range(length):
        response = br.open(sub_cat_url[i])
        soup = BeautifulSoup(response)
        sub_cat_item_list = []
        for tag in soup.find_all('th', 'new'):
            href = tag.find('a', 's xst')
            title = href.get_text()
            link = href.get('href')
            sub_cat_item_list.append((title, base_url + link))
        data.append((sub_cat_name[i], sub_cat_item_list))
    return data

def csdn_crawer(br):
    sub_cat_url = (
        'http://blog.csdn.net/mobile/index.html?&page=',
        'http://blog.csdn.net/mobile/newest.html?&page='
        )
    sub_cat_name = (u'最热',u'最新')
    length = len(sub_cat_name)
    data = []
    for i in range(length):
        baseurl = sub_cat_url[i]
        sub_cat_item_list = []
        for j in range(1,10):
            response = br.open(baseurl+str(j))
            soup = BeautifulSoup(response)
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
                sub_cat_item_list.append((cat + title,url))
        data.append((sub_cat_name[i], sub_cat_item_list))
    return data

if __name__ == '__main__':
    # 浏览器伪装
    br = mechanize.Browser()
    br.set_handle_equiv(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.addheaders = [('User-agent',
                      'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

    file = open('[' + time.strftime('%Y%m%d') + ']AndroidNews.html', 'a')
    data = csdn_crawer(br)

    # 遍历分类
    for i in range(len(data)):
        # 打印分类
        file.write('<h2>%s</h2>' % data[i][0])
        # 遍历分类下条目
        for j in range(len(data[i][1])):
            # 打印条目
            file.write('<p><a href="' + data[i][1][j][1] + '">' + data[i][1][j][0] + '</a></p>')
    file.close()