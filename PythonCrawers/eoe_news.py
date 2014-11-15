__author__ = 'maxiee'
# -*- coding: UTF-8 -*-
import mechanize
from bs4 import BeautifulSoup
import time

'''
程序功能：抓取EOE社区各专题热门第一页
'''

#设置Python编码，否则不能创建文件
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

br = mechanize.Browser()
br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)


base_url = 'http://www.eoeandroid.com/'

def scratch(url):
    response = br.open(url)
    soup = BeautifulSoup(response)
    i=0
    for tag in soup.find_all('th','new'):
        href = tag.find('a','s xst')
        title = href.get_text()
        link = href.get('href')
        print(u'%3d.名称:' % i+title)
        print(u'    链接:'+base_url+link+'\n')
        i += 1

if __name__ == "__main__":
    print(u"新手入门:\n")
    scratch('http://www.eoeandroid.com/forum.php?mod=forumdisplay&fid=53&filter=lastpost&orderby=lastpost')

    print(u"经验分享:\n")
    scratch('http://www.eoeandroid.com/forum.php?mod=forumdisplay&fid=93&filter=lastpost&orderby=lastpost')

    print(u"开发问答:\n")
    scratch('http://www.eoeandroid.com/forum.php?mod=forumdisplay&fid=45&filter=lastpost&orderby=lastpost')

    print(u"实例教程:\n")
    scratch('http://www.eoeandroid.com/forum.php?mod=forumdisplay&fid=27&filter=lastpost&orderby=lastpost')

    print(u"盈利模式:\n")
    scratch('http://www.eoeandroid.com/forum.php?mod=forumdisplay&fid=89&filter=lastpost&orderby=lastpost')

    print(u"源码分享:\n")
    scratch('http://www.eoeandroid.com/forum.php?mod=forumdisplay&fid=23&filter=lastpost&orderby=lastpost')

    print(u"资料分享:\n")
    scratch('http://www.eoeandroid.com/forum.php?mod=forumdisplay&fid=15&filter=lastpost&orderby=lastpost')

    print(u"UI界面:\n")
    scratch('http://www.eoeandroid.com/forum.php?mod=forumdisplay&fid=208&filter=lastpost&orderby=lastpost')

    print(u"开源项目:\n")
    scratch('http://www.eoeandroid.com/forum.php?mod=forumdisplay&fid=207&filter=lastpost&orderby=lastpost')

    print(u"视频教程:\n")
    scratch('http://www.eoeandroid.com/forum.php?mod=forumdisplay&fid=200&filter=lastpost&orderby=lastpost')

    print(u"电子图书:\n")
    scratch('http://www.eoeandroid.com/forum.php?mod=forumdisplay&fid=843&filter=lastpost&orderby=lastpost')

    print(u"游戏开发:\n")
    scratch('http://www.eoeandroid.com/forum.php?mod=forumdisplay&fid=182&filter=lastpost&orderby=lastpost')

    print(u"Cocos2D:\n")
    scratch('http://www.eoeandroid.com/forum.php?mod=forumdisplay&fid=808&filter=lastpost&orderby=lastpost')