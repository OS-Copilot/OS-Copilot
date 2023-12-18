from bs4 import BeautifulSoup
import requests
import re
import json
from typing import Tuple

url = "https://en.wikipedia.org/wiki/Mercedes_Sosa"


def web_browser( url: str, max_retry: int = 3) -> Tuple[bool, str]:
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
    for _ in range(max_retry):
        try:
            res = requests.get(url,headers=headers, timeout=15)
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

# # url = "https://learn.microsoft.com/en-us/bing/search-apis/bing-web-search/reference/endpoints"
# state, page_detail = web_browser(url=url)
# print(page_detail)
# print("共{}个字符".format(len(page_detail)))

# with open("test.json", "w", encoding="utf-8") as f:
#     json.dump(page_detail, f, ensure_ascii=False, indent=4)
