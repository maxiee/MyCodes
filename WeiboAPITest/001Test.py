__author__ = 'Maxiee'

import requests

token = input("Token>")

print(token)

response = requests.get("https://api.weibo.com/2/statuses/home_timeline.json?count=20&page=1&access_token="+token)

print(response.text)