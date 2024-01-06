import requests
class ToolRequestUtil:
    def __init__(self):
        self.session = requests.session()
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
        self.base_url = "http://43.159.144.130:8079"

    def request(self, api_path, method, params=None, files=None, content_type=None):
        """
        :param api_path: the path of the api
        :param method: get/post
        :param params: the params of the api, can be None
        :param files: files to be uploaded, can be None
        :param content_type: the content_type of api, e.g., application/json, multipart/form-data, can be None
        :return: the return of the api
        """
        url = self.base_url + api_path
        try:
            # 判断请求方法
            if method.lower() == "get":
                if content_type == "application/json":
                    result = self.session.get(url=url, json=params, headers=self.headers).json()
                else: 
                    result = self.session.get(url=url, params=params, headers=self.headers).json()
            elif method.lower() == "post":
                if content_type == "multipart/form-data":
                    result = self.session.post(url=url, files=files, data=params, headers=self.headers).json()
                elif content_type == "application/json":
                    result = self.session.post(url=url, json=params, headers=self.headers).json()
                else:
                    result = self.session.post(url=url, data=params, headers=self.headers).json()
            else:
                print("request method error!")
                return None
            return result
        except Exception as e:
            print("http request error：%s" % e)
            return None