from bs4 import BeautifulSoup
import requests
import re
import json
from typing import Tuple
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
# url = "https://en.wikipedia.org/wiki/Mercedes_Sosa"
# with open("../../examples/config.json") as f:
#     config = json.load(f)
# embeddings = OpenAIEmbeddings(
#             openai_api_key=config['OPENAI_API_KEY'],
#             openai_organization=config['OPENAI_ORGANIZATION'],
#         )
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
        return "Timeout for loading this page, Please try to load another one or search again."
    try:
        soup = BeautifulSoup(content, 'html.parser')
        # paragraphs = soup.find_all('p')
        # page_detail = ""
        # for p in paragraphs:
        #     text = p.get_text().strip()
        #     page_detail += text
        # if(len(page_detail) < 40):
        page_detail = soup.getText()
        page_detail = re.sub(r'\s+', ' ', page_detail)
        page_detail = re.sub(r'\n\s*\n', '\n', page_detail)
        # text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        # texts = text_splitter.create_documents([page_detail])
        # docsearch = Chroma.from_documents(texts, embeddings)
        # docs = docsearch.similarity_search(query, k=5)

        return page_detail
    except Exception:
        return "Timeout for loading this page, Please try to load another one or search again."

url = "https://zhuanlan.zhihu.com/p/541484549"
page_detail = web_browser(url=url)
print(page_detail)
print("共{}个字符".format(len(page_detail)))

# with open("test.json", "w", encoding="utf-8") as f:
#     json.dump(page_detail, f, ensure_ascii=False, indent=4)
