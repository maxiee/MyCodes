__author__ = 'Maxiee'

import cookielib
import urllib
import urllib2

ID_USERNAME = 'text'
ID_PASSWORD = 'password'

USERNAME =  raw_input('user>')
PASSWORD = raw_input('passwd>')

LOGIN_URL='http://weibo.com/'
URL2 = 'http://weibo.com/maxiee/home?topnav=1&wvr=6'

cj = cookielib.CookieJar()

login_data = urllib.urlencode({ID_USERNAME:USERNAME,\
                               ID_PASSWORD:PASSWORD})

opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
resp = opener.open(LOGIN_URL, login_data)

for cookie in cj:
    print cookie.name + ": "+cookie.value

print resp.headers