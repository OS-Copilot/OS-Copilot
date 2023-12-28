import requests
class ToolRequestUtil:
    def __init__(self):
        self.session = requests.session()
        self.headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
        self.base_url = "http://43.159.144.130:8079"
    def request(self , api_path , method , params=None , content_type=None):
        """
        :param api_path: the path of the api
        :param method: get/post
        :param params: the params of the api, can be None
        :param content_type : the content_type of api,eg. application/json, can be None
        :return: the return of the api
        """
        url = self.base_url + api_path
        try:
            #判断请求方法
            if method == "get":
                if content_type == "application/json":
                    result = self.session.get(url=url, json=params, headers=self.headers).json()
                else: 
                    result = self.session.get(url=url, params=params, headers=self.headers).json()
            elif method == "post":
                if content_type == "application/json":
                    result = self.session.post(url=url, json=params, headers=self.headers).json()
                else:
                    result = self.session.post(url=url, data=params, headers=self.headers).json()
            else:
                print("request method error!")
            return result
        except Exception as e:
            print("http request error：%s"%e)

if __name__ == '__main__':
    #post请求 创建一个实例r
    api_path = "/tools/bing/load_pagev2"
    r = ToolRequestUtil()
    data = {
  # 'url': 'https://blog.csdn.net/sjxgghg/article/details/134312033',
  # 'query': '如何解决这个bug?',
  'query': 'Mercedes Sosa studio albums 2000-2009',
  'url':'https://en.wikipedia.org/wiki/Mercedes_Sosa'
}
    content_type = "application/json"
    response = r.request(api_path, 'get', params=data, content_type=content_type)
    print(response)
 
