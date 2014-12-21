__author__ = 'Maxiee'
# -*- coding: UTF-8 -*-

import mechanize
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import jieba
import matplotlib.pyplot as pyplot
import matplotlib
import os
import re
import codecs

'''
程序功能：

    抓取人民日报历史数据进行词频统计
    人民日报历史数据来源：http://rmrbw.info/
'''
#TODO 在线数据来源占用网络资源太大，采用微盘提供的数据库文件较好
#TODO 文件链接： http://vdisk.weibo.com/s/uFevWCo592dYx

# 创建缓存文件夹
CONTENT_ROOT_PATH = 'content/'
if not os.path.exists(CONTENT_ROOT_PATH):
    os.makedirs(CONTENT_ROOT_PATH)

# 浏览器伪装
br = mechanize.Browser()
br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.addheaders = [('User-agent',
                  'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)')]

ROOT_URL = 'http://rmrbw.info/'

# 指定年份上下限
# 如果只需要抓取某一年，只需令两个变量均等于这一年
year_low = 1946
year_high = 1946

# 待分词的新闻
content = ''

response = br.open(ROOT_URL)
soup = BeautifulSoup(response)
soup = soup.find('div','contentwrap')

all_years_tags = soup.find_all('div','t')


def get_month_news(url):
    response = br.open(url)
    soup = BeautifulSoup(response)
    page_total = soup.find('div', 'pages').get_text().split(' ')[-4].split('/')[1]
    soup = soup.find('div','t')
    page_total = int(page_total)
    news_urls = []
    news_titles = []
    # 获取当月所有的新闻标题和链接
    for page_index in range(2,page_total+2):
        for tag in soup.find_all('h3'):
            # 文章标题
            news_titles.append(tag.get_text())
            # 文章链接
            news_urls.append(ROOT_URL + tag.a.get('href'))
        page_url = url + '&page=' + str(page_index)
        response = br.open(page_url)
        soup = BeautifulSoup(response)
    return news_titles,news_urls


def craw_news(news_titles, news_urls,month_dir):
    # 待分词新闻内容
    content = ''
    if not os.path.exists(month_dir):
        os.makedirs(month_dir)
    FILE_FIX = '.txt'
    for index in range(len(news_urls)):
        print u"正在加载第[%d/%d]条" %(index,len(news_urls)-1),
        file_path = month_dir + news_titles[index]+FILE_FIX
        if os.path.exists(file_path):
            print u'加载本地缓存...'
            f = codecs.open(file_path,'r','utf-8')
            news_content = f.read()
            f.close()
        else:
            print u'在线抓取...'
            response = br.open(news_urls[index])
            soup = BeautifulSoup(response)
            soup = soup.find('div','tpc_content')
            # 内容全文
            news_content = soup.get_text().strip()
            f = codecs.open(file_path,'w','utf-8')
            f.write(news_content)
            f.close()
        content += news_content
    return content


# 根据年限开始抓取
for i in range(year_high-year_low+1):
    year_tag = all_years_tags[i]
    # month_tags 第一个元素为年份，剩下为月份
    month_tags = year_tag.find_all('h2')
    year = month_tags[0].get_text()
    print u'正在抓取'+ year +u'...',
    year_dir = CONTENT_ROOT_PATH + year +'/'
    if not os.path.exists(year_dir):
        os.makedirs(year_dir)
    del month_tags[0]
    # 遍历当年所有月份
    for month_tag in month_tags:
        current_month = month_tag.get_text()
        print u'正在抓取'+ current_month
        month_dir = year_dir + current_month + '/'
        url = ROOT_URL + month_tag.a.get('href')
        print url
        # 当月新闻标题与链接
        news_titles,news_urls = get_month_news(url)
        # 抓取当月所有新闻
        content += craw_news(news_titles,news_urls,month_dir)

# 词频统计
# 创建黑名单，用户过滤
blacklist = [u'看似', u'关系', u'这本', u'接连', u'其', u'》', u'第一', u'第二', u'第三', u'第四', u'应',
             u'是', u'也', u'上', u'后', u'前', u'我台', u'再', u',', u'以及', u'因为', u'从而', u'但', u'像',
             u'更', u'用', u'“', u'这', u'有', u'在', u'去', u'都', u'”', u'还', u'使', u'，', u'把', u'向',
             u'中', u'新', u'对', u'　', u' ', u')', u'、', u'。', u';', u'%', u'：', u'?', u'(', u'的',
             u'和', u'了', u'等', u'将', u'到', u'', u'央视网', u'新闻联播', u'正在', u'我国', u'通过',
             u'国际', u'从', u'年', u'今天', u'要', u'并', u'\n', u'《', u'为', u'月', u'号', u'日', u'大']
hist = {}
for word in jieba.cut(content):
    if word in blacklist:
        continue
    hist[word] = hist.get(word, 0) + 1

# matplotlib Windows下中文字体
font = matplotlib.font_manager.FontProperties(fname='c:\\windows\\fonts\\simsun.ttc')

# 打印分词结果，用于调试，创建黑名单
# for key in hist.keys():
#     print(key)

# 对词频排序
hist_sorted = sorted(hist.iteritems(), key=lambda d: d[1], reverse=True)
# 取频率最高的50个词绘制曲线图
print "正在绘制柱状图..."
bar_width = 0.35
pyplot.bar(range(20), [hist_sorted[i][1] for i in range(20)],bar_width)
pyplot.xticks(range(20), [hist_sorted[i][0] for i in range(20)], fontproperties=font,rotation=30)
pyplot.title(u"《人民日报》词频分析" + u"by Maxiee",fontproperties=font)
pyplot.show()