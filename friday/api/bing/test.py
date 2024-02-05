import requests

# response = requests.get(
#     'http://127.0.0.1:8079/tools/bing/search',
#     json={'query': 'Python'}
# )
# print(response.json())

# response = requests.get(
#     'http://127.0.0.1:8079/tools/bing/load_page',
#     json={'url': 'https://www.python.org/'}
# )
# print(response.json())
import requests
import json

headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
# url="http://101.132.188.137:8079/test?q=1"
url="http://101.132.188.137:8079/tools/bing/load_pagev2"
param = {
  'url': 'https://blog.csdn.net/sjxgghg/article/details/134312033',
}
res = requests.get(url,
                   headers=headers,
                   json=param,
                     timeout=30)
print(res.text)