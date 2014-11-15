__author__ = 'maxiee'

import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

url = "http://www.baidu.com/s"
values = {'wd':"Kindle电子书"}
encoded_param = urllib.parse.urlencode(values)
full_url = url + '?' + encoded_param
response = urllib.request.urlopen(full_url)
soup = BeautifulSoup(response)
alinks = soup.find_all('a')
print(alinks)