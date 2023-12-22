import requests


headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
url="http://10.241.41.203:8079/tools/bing/searchv2"
res = requests.get(url,
                   headers=headers,
                    json={'query': 'Python'},
                     timeout=15)
print(res)