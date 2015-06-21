from urllib.request import urlopen, Request, build_opener, install_opener, ProxyHandler
from bs4 import BeautifulSoup

BASE_URL = 'http://developer.android.com/training'

def exrtract_page(url):
    proxies = {'http': '127.0.0.1:8118'}
    proxy = ProxyHandler(proxies)
    opener = build_opener(proxy)
    install_opener(opener)

    request = Request(url)
    content = urlopen(request, timeout=30).read()
    soup = BeautifulSoup(content)

    header = \
        '<h1>' \
        + soup.find('h1', {'itemprop': 'name'}).get_text() \
        + '</h1>\n'

    main_content = soup.find('div', {'itemprop': 'articleBody'}).prettify(formatter='html')
    main_content = main_content.replace('/images/', 'http://developer.android.com/images/')

    output = open('output.html', 'w')
    output.write(
            header
            + main_content)

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
            sec_list = list(item.ul.children)
            for sec_item in sec_list:
                # 二级标题
                if sec_item.name == 'li':
                    sec_title = " ".join(sec_item.a.get_text().strip().replace('\n','').split())
                    print('\t2级:' + sec_title)
                    exrtract_page(sec_item.a.get('href'))
                    return
                    # print('('+sec_item.a.get('href')+')')
                    if sec_item.ul is not None:
                        thir_list = list(sec_item.ul.children)
                        for thir_item in thir_list:
                            # 三级标题
                            if thir_item.name == 'li':
                                thir_title = " ".join(thir_item.a.get_text().strip().replace('\n','').split())
                                print('\t\t3级:' + thir_title)
                                #print('('+thir_item.a.get('href')+')')



parse_content()
