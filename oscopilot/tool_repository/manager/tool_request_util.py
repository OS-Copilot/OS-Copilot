import requests
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env', override=True)
API_BASE_URL = os.getenv('API_BASE_URL') 

class ToolRequestUtil:
    """
    A utility class for making HTTP requests to an API.

    This class simplifies the process of sending HTTP requests using a persistent session
    and predefined headers, including a User-Agent header to mimic a browser request. It's
    designed to interact with APIs by sending GET or POST requests and handling file uploads.

    Attributes:
        session (requests.Session): A requests session for making HTTP requests.
        headers (dict): Default headers to be sent with each request.
        base_url (str): The base URL for the API endpoints.
    """
    def __init__(self):
        """
        Initializes the ToolRequestUtil with a session and default request headers.
        """
        self.session = requests.session()
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
        self.base_url = API_BASE_URL

    def request(self, api_path, method, params=None, files=None, content_type="application/json"):
        """
        Sends a request to the specified API endpoint using the defined HTTP method.

        This method constructs the request URL from the base URL and the API path. It supports
        both GET and POST methods, including handling of JSON parameters, file uploads, and
        different content types.

        Args:
            api_path (str): The path of the API endpoint.
            method (str): The HTTP method to use for the request ('get' or 'post').
            params (dict, optional): The parameters to include in the request. Defaults to None.
            files (dict, optional): Files to be uploaded in a POST request. Defaults to None.
            content_type (str, optional): The content type of the request, such as
                'application/json' or 'multipart/form-data'. Defaults to "application/json".

        Returns:
            dict: The JSON response from the API, or None if an error occurs.

        Raises:
            Prints an error message to the console if an HTTP request error occurs.
        """
        url = self.base_url + api_path
        try:
            if method.lower() == "get":
                if content_type == "application/json":
                    result = self.session.get(url=url, json=params, headers=self.headers, timeout=60).json()
                else: 
                    result = self.session.get(url=url, params=params, headers=self.headers, timeout=60).json()
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
            print("http request error: %s" % e)
            return None