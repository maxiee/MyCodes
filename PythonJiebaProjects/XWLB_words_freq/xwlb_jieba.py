__author__ = 'Maxiee'
# -*- coding: UTF-8 -*-

import mechanize
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import jieba
import matplotlib.pyplot as pyplot
import matplotlib

# 昨天日期
yesterday = datetime.now() - timedelta(days=1)

ROOT_URL = 'http://cctv.cntv.cn/lm/xinwenlianbo/' + yesterday.strftime('20%y%m%d') + '.shtml'
print "新闻目录URL：", ROOT_URL

# 浏览器伪装
br = mechanize.Browser()
br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.addheaders = [('User-agent',
                  'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

# 新闻联播中各条具体新闻链接
response = br.open(ROOT_URL)
soup = BeautifulSoup(response)
soup = soup.find('div', 'md_bd')
news_urls = []
count = 0

print '正在获取昨日新闻列表...'
# 抓取各条具体新闻链接
for tag_li in soup.find_all('li'):
    # 避开新闻联播全文
    if count == 0:
        count += 1
        continue
    news_urls.append(tag_li.a.get('href'))
    count += 1
print u"昨日共%d条新闻。" % len(news_urls)

print '正在获取新闻联播内容...'
news_count = 1
# 主要内容
content = ''
for url in news_urls:
    print "[%d/%d]获取中..." % (news_count, len(news_urls)),
    response = br.open(url)
    soup = BeautifulSoup(response)
    soup = soup.find('div', 'body')
    content += soup.get_text()
    print "ok!"
    news_count += 1
# print content

print "正在分词并进行词频统计..."
# 创建黑名单，用户过滤
blacklist = [u'看似', u'关系', u'这本', u'接连', u'其', u'》', u'第一', u'第二', u'第三', u'第四', u'应',
             u'是', u'也', u'上', u'后', u'前', u'我台', u'再', u',', u'以及', u'因为', u'从而', u'但', u'像',
             u'更', u'用', u'“', u'这', u'有', u'在', u'去', u'都', u'”', u'还', u'使', u'，', u'把', u'向',
             u'中', u'新', u'对', u'　', u' ', u')', u'、', u'。', u';', u'%', u'：', u'?', u'(', u'的',
             u'和', u'了', u'等', u'将', u'到', u'', u'央视网', u'新闻联播', u'正在', u'我国', u'通过',
             u'国际', u'从', u'年', u'今天', u'要', u'并', u'\n']
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
pyplot.show()
# 打印分词结果，用于调试，创建黑名单
# for i in range(30):
#     print hist_sorted[i][0]
# print  hist_sorted
