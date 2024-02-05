import os

class ConfigManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance.http_proxy = "http://127.0.0.1:10809"
            cls._instance.https_proxy = "http://127.0.0.1:10809"
            # cls._instance.http_proxy = None
            # cls._instance.https_proxy = None
        return cls._instance

    def set_proxies(self, http, https):
        self.http_proxy = http
        self.https_proxy = https

    def apply_proxies(self):
        if self.http_proxy:
            os.environ["http_proxy"] = self.http_proxy
        if self.https_proxy:
            os.environ["https_proxy"] = self.https_proxy

    def clear_proxies(self):
        os.environ.pop("http_proxy", None)
        os.environ.pop("https_proxy", None)

