from urllib.request import urlopen, Request, build_opener, install_opener, ProxyHandler
from bs4 import BeautifulSoup
import os.path

BASE_TRAINING = 'http://developer.android.com/training'
BASE_GUIDE = 'http://developer.android.com/guide'

BASE_URL = BASE_TRAINING

HTML_dir = 'html/'

info_page = []
info_title = []
info_class = []

count = 1

def exrtract_page(url, title):
    proxies = {'http': '127.0.0.1:8118'}
    proxy = ProxyHandler(proxies)
    opener = build_opener(proxy)
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    install_opener(opener)

    file_path = HTML_dir + title + '.html'
    if os.path.exists(file_path):
        return

    request = Request(url)
    content = urlopen(request, timeout=30).read()
    soup = BeautifulSoup(content)

    page_title = soup.find('h1', {'itemprop': 'name'}).get_text()
    header = \
        '<h1>' \
        + page_title \
        + '</h1>\n'

    main_content = soup.find('div', {'itemprop': 'articleBody'}).prettify(formatter='html')
    main_content = main_content.replace('/images/', 'http://developer.android.com/images/')

    output = open(file_path, 'w')
    output.write(
            header
            + main_content)

def exrtract_multi_pages(urls, title):
    proxies = {'http': '127.0.0.1:8118'}
    proxy = ProxyHandler(proxies)
    opener = build_opener(proxy)
    install_opener(opener)

    file_path = HTML_dir + title + '.html'
    all_content = ""
    for url in urls:
        print("extracting %s" % url)
        request = Request(url)
        content = urlopen(request, timeout=30).read()
        if content is not None:
            print("返回结果不为空")
        soup = BeautifulSoup(content)

        page_title = soup.find('h1', {'itemprop': 'name'}).get_text()
        header = \
            '<h1>' \
            + page_title \
            + '</h1>\n'

        main_content = soup.find('div', {'itemprop': 'articleBody'}).prettify(formatter='html')
        #main_content = main_content.replace('/images/', 'http://developer.android.com/images/')
        main_content = main_content.replace(' src="', ' src="http://developer.android.com/')
        all_content += header + main_content

    output = open(file_path, 'w')
    output.write(all_content)

def add_content(page, title, cls):
    info_page.append(page)
    info_title.append(title)
    info_title.append(cls)

def parse_content():
    content = open('contents.html', 'r').read()
    soup = BeautifulSoup(content)
    contents = soup.find('ul', {'id': 'nav'})
    nav_list = list(contents.children)
    for item in nav_list:
        if item.name == 'li':
            # 一级标题
            title = " ".join(item.div.a.get_text().strip().replace('\n','').split())
            print('\n1级:' + title)
            #print('('+item.div.a.get('href')+')')
            exrtract_page(item.div.a.get('href'), title)
            add_content(count, title, 1)
            count += 1
            sec_list = list(item.ul.children)
            for sec_item in sec_list:
                # 二级标题
                if sec_item.name == 'li':
                    sec_title = " ".join(sec_item.a.get_text().strip().replace('\n','').split())
                    print('\t2级:' + sec_title)
                    exrtract_page(sec_item.a.get('href'), sec_title)
                    add_content(count, sec_title, 2)
                    count += 1
                    # print('('+sec_item.a.get('href')+')')
                    if sec_item.ul is not None:
                        thir_list = list(sec_item.ul.children)
                        for thir_item in thir_list:
                            # 三级标题
                            if thir_item.name == 'li':
                                thir_title = " ".join(thir_item.a.get_text().strip().replace('\n','').split())
                                print('\t\t3级:' + thir_title)
                                #print('('+thir_item.a.get('href')+')')
                                exrtract_page(thir_item.a.get('href'), thir_title)
                                add_content(count, thir_title, 3)
                                count += 1



#parse_content()

urls = [
        "http://developer.android.com/intl/zh-cn/training/wearables/watch-faces/index.html",
        "http://developer.android.com/intl/zh-cn/training/wearables/watch-faces/designing.html",
        "http://developer.android.com/intl/zh-cn/training/wearables/watch-faces/service.html",
        "http://developer.android.com/intl/zh-cn/training/wearables/watch-faces/drawing.html",
        "http://developer.android.com/intl/zh-cn/training/wearables/watch-faces/information.html",
        "http://developer.android.com/intl/zh-cn/training/wearables/watch-faces/interacting.html",
        "http://developer.android.com/intl/zh-cn/training/wearables/watch-faces/configuration.html",
        "http://developer.android.com/intl/zh-cn/training/wearables/watch-faces/issues.html",
        "http://developer.android.com/intl/zh-cn/training/wearables/watch-faces/performance.html"
        ]

exrtract_multi_pages(urls, "1")
