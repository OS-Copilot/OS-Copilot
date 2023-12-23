import requests
import json

headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
# url="http://101.132.188.137:8079/test?q=1"
# url="http://101.132.188.137:8079/tools/bing/load_pagev2"
url="http://10.241.41.203:8079/tools/bing/load_pagev2"
# url="http://192.168.31.128:8079/tools/bing/searchv2"
# param = {
#   # 'url': 'https://blog.csdn.net/sjxgghg/article/details/134312033',
#   # 'query': '如何解决这个bug?',
#   'query': 'Mercedes Sosa studio albums 2000-2009',
#   'url':'https://en.wikipedia.org/wiki/Mercedes_Sosa'
# }
param = {
  'url': 'https://blog.csdn.net/sjxgghg/article/details/134312033',
  'query': '如何解决这个bug?',
  # 'query': '2015',
  # 'url':'https://en.wikipedia.org/wiki/OpenAI'
}
res = requests.get(url,
                   headers=headers,
                   json=param,
                     timeout=30)
print(res.text)