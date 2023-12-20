import requests


headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
url="http://101.132.188.137:8079/tools/bing/search"
res = requests.get(url,
                   headers=headers,
                    json={'query': 'Python'},
                     timeout=15)
print(res.text)