import requests
from bs4 import BeautifulSoup
from typing import Tuple
from enum import Enum

SEARCH_RESULT_LIST_CHUNK_SIZE = 3
RESULT_TARGET_PAGE_PER_TEXT_COUNT = 500


class ImageSearchAPI:
    def __init__(self, subscription_key: str) -> None:
        self._headers = {
            'Ocp-Apim-Subscription-Key': subscription_key,
            'BingAPIs-Market': 'en-US',
            
        }
        self._endpoint = "https://api.bing.microsoft.com/v7.0/images/search"
        self._mkt = 'en-US'

    def search_image(self, key_words: str,top_k: int=10, max_retry: int = 3):
        
        for _ in range(max_retry):
            try:
                result = requests.get(self._endpoint, headers=self._headers, params={'q': key_words, 'mkt': self._mkt,'safeSearch' : 'moderate'},
                                      timeout=10)
            except Exception:
                continue
            if result.status_code == 200:
                result = result.json()
                image_List = []
                if result != None:
                    image_List = [
                        {
                            "imageName": item["name"],
                            "imageUrl": item["thumbnailUrl"],
                            "imageSize": item["thumbnail"]
                        } for item in result["value"]
                    ]
                    if(len(image_List) > top_k):
                        image_List = image_List[:top_k]
                return image_List
            else:
                continue
        raise RuntimeError("Failed to access Bing Search API.")
 
