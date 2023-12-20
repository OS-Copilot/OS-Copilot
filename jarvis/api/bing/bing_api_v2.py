import requests
from langchain.utilities import BingSearchAPIWrapper
from bs4 import BeautifulSoup
from typing import Tuple
from enum import Enum
from web_loader import WebPageLoader
import os

os.environ["BING_SUBSCRIPTION_KEY"] = "885e62a126554fb390af88ae31d2c8ff"
os.environ["BING_SEARCH_URL"] = "https://api.bing.microsoft.com/v7.0/search"

SEARCH_RESULT_LIST_CHUNK_SIZE = 3
RESULT_TARGET_PAGE_PER_TEXT_COUNT = 500


class BingAPIV2:
    def __init__(self) -> None:
        self.search_engine = BingSearchAPIWrapper()
        self.web_loader = WebPageLoader()

    def search(self, key_words: str,top_k: int = 5, max_retry: int = 3):
            # return search.results(query,top_k)
        for _ in range(max_retry):
            try:
                result = self.search_engine.results(key_words,top_k)
            except Exception:
                continue
            if result != None:
                return result
            else:
                continue
        raise RuntimeError("Failed to access Bing Search API.")

    def load_page(self, url: str) -> str:
        page_data = self.web_loader.load_data(url)
        page_content_str = ""
        if(page_data["data"][0] != None and page_data["data"][0]["content"] != None):
            page_content_str = page_data["data"][0]["content"]
        return page_content_str
    def summarize_loaded_page(self,page_str):
        pass
    def attended_loaded_page(self,page_str,query_str):
        pass