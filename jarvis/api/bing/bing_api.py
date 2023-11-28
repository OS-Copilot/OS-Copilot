import requests
from bs4 import BeautifulSoup
from typing import Tuple
from enum import Enum

SEARCH_RESULT_LIST_CHUNK_SIZE = 3
RESULT_TARGET_PAGE_PER_TEXT_COUNT = 500


class BingAPI:
    def __init__(self, subscription_key: str) -> None:
        self._headers = {
            'Ocp-Apim-Subscription-Key': subscription_key
        }
        self._endpoint = "https://api.bing.microsoft.com/v7.0/search"
        self._mkt = 'en-US'

    def search(self, key_words: str, max_retry: int = 3):
        for _ in range(max_retry):
            try:
                result = requests.get(self._endpoint, headers=self._headers, params={'q': key_words, 'mkt': self._mkt},
                                      timeout=10)
            except Exception:
                continue
            if result.status_code == 200:
                result = result.json()
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
