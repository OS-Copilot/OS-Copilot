import requests
from langchain.utilities import BingSearchAPIWrapper
from bs4 import BeautifulSoup
from typing import Tuple
from enum import Enum
import os

os.environ["BING_SUBSCRIPTION_KEY"] = "885e62a126554fb390af88ae31d2c8ff"
os.environ["BING_SEARCH_URL"] = "https://api.bing.microsoft.com/v7.0/search"

SEARCH_RESULT_LIST_CHUNK_SIZE = 3
RESULT_TARGET_PAGE_PER_TEXT_COUNT = 500


class BingAPIV2:
    def __init__(self) -> None:
        self.search_engine = BingSearchAPIWrapper()

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

    def load_page(self, url: str, max_retry: int = 3) -> Tuple[bool, str]:
        for _ in range(max_retry):
            try:
                res = requests.get(url, timeout=15)
                if res.status_code == 200:
                    res.raise_for_status()
                else:
                    raise RuntimeError("Failed to load page, code {}".format(res.status_code))
            except Exception:
                res = None
                continue
            res.encoding = res.apparent_encoding
            content = res.text
            break
        if res is None:
            return False, "Timeout for loading this page, Please try to load another one or search again."
        try:
            soup = BeautifulSoup(content, 'html.parser')
            paragraphs = soup.find_all('p')
            page_detail = ""
            for p in paragraphs:
                text = p.get_text().strip()
                page_detail += text
            return True, page_detail
        except Exception:
            return False, "Timeout for loading this page, Please try to load another one or search again."
    def summarize_loaded_page():
        pass
    def attended_loaded_page():
        pass