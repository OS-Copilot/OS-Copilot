import requests
from langchain.utilities import BingSearchAPIWrapper
from bs4 import BeautifulSoup
from typing import Tuple
from enum import Enum
from .web_loader import WebPageLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains.summarize import load_summarize_chain
from langchain import OpenAI
import os

# Set bing search and OpenAPI Key
os.environ["BING_SUBSCRIPTION_KEY"] = ""
os.environ["BING_SEARCH_URL"] = "https://api.bing.microsoft.com/v7.0/search"
os.environ["OPENAI_API_KEY"] = ""
os.environ["OPENAI_ORGANIZATION"] = ""

SEARCH_RESULT_LIST_CHUNK_SIZE = 3
RESULT_TARGET_PAGE_PER_TEXT_COUNT = 500


class BingAPIV2:
    def __init__(self) -> None:
        self.search_engine = BingSearchAPIWrapper(search_kwargs={'mkt': 'en-us','safeSearch': 'moderate'})
        self.web_loader = WebPageLoader()
        self.web_chunker = RecursiveCharacterTextSplitter(chunk_size=4500, chunk_overlap=0)
        self.web_sniptter_embed = OpenAIEmbeddings()
        self.web_summarizer = OpenAI(
            temperature=0,
            )

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
        if page_str == "":
            return ""
        web_chunks = self.web_chunker.create_documents([page_str])
        summarize_chain = load_summarize_chain(self.web_summarizer, chain_type="map_reduce")
        main_web_content = summarize_chain.run(web_chunks)
        return main_web_content
    def attended_loaded_page(self,page_str,query_str):
        if page_str == "":
            return ""
        web_chunks = self.web_chunker.create_documents([page_str])
        chunSearch = Chroma.from_documents(web_chunks, self.web_sniptter_embed)
        relatedChunks = chunSearch.similarity_search(query_str, k=3)
        attended_content = '...'.join([chunk.page_content for chunk in relatedChunks])
        return attended_content


