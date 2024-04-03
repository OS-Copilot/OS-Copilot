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

SEARCH_RESULT_LIST_CHUNK_SIZE = 3
RESULT_TARGET_PAGE_PER_TEXT_COUNT = 500


class BingAPIV2:
    """
    A class for interacting with the Bing Search API and performing subsequent processing on web page data.

    This class encapsulates the functionality to perform web searches using Bing's API, load web pages,
    chunk and embed text for analysis, summarize web pages, and attend to loaded pages based on specific queries.

    Attributes:
        search_engine (BingSearchAPIWrapper): Configured instance for executing searches with Bing's API.
        web_loader (WebPageLoader): Utility for loading web page content.
        web_chunker (RecursiveCharacterTextSplitter): Utility for splitting text into manageable chunks.
        web_sniptter_embed (OpenAIEmbeddings): Embedding model for text chunks.
        web_summarizer (OpenAI): Model for summarizing web page content.
    """
    def __init__(self) -> None:
        """
        Initializes the BingAPIV2 with components for search, web page loading, and text processing.
        """
        self.search_engine = BingSearchAPIWrapper(search_kwargs={'mkt': 'en-us','safeSearch': 'moderate'})
        self.web_loader = WebPageLoader()
        self.web_chunker = RecursiveCharacterTextSplitter(chunk_size=4500, chunk_overlap=0)
        self.web_sniptter_embed = OpenAIEmbeddings()
        self.web_summarizer = OpenAI(
            temperature=0,
            )

    def search(self, key_words: str,top_k: int = 5, max_retry: int = 3):
        """
        Searches for web pages using Bing's API based on provided keywords.

        Attempts the search up to a specified number of retries upon failure.

        Args:
            key_words (str): The keywords to search for.
            top_k (int, optional): The number of search results to return. Defaults to 5.
            max_retry (int, optional): The maximum number of retry attempts. Defaults to 3.

        Returns:
            list: A list of search results.

        Raises:
            RuntimeError: If the search attempts fail after reaching the maximum number of retries.
        """
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
        """
        Loads the content of a web page given its URL.

        Args:
            url (str): The URL of the web page to load.

        Returns:
            str: The content of the web page as a string.
        """
        page_data = self.web_loader.load_data(url)
        page_content_str = ""
        if(page_data["data"][0] != None and page_data["data"][0]["content"] != None):
            page_content_str = page_data["data"][0]["content"]
        return page_content_str
    def summarize_loaded_page(self,page_str):
        """
        Summarizes the content of a loaded web page.

        Args:
            page_str (str): The content of the web page to summarize.

        Returns:
            str: The summarized content of the web page.
        """
        if page_str == "":
            return ""
        web_chunks = self.web_chunker.create_documents([page_str])
        summarize_chain = load_summarize_chain(self.web_summarizer, chain_type="map_reduce")
        main_web_content = summarize_chain.run(web_chunks)
        return main_web_content
    def attended_loaded_page(self,page_str,query_str):
        """
        Identifies and aggregates content from a loaded web page that is most relevant to a given query.

        Args:
            page_str (str): The content of the web page.
            query_str (str): The query string to identify relevant content.

        Returns:
            str: The aggregated content from the web page that is most relevant to the query.
        """
        if page_str == "":
            return ""
        web_chunks = self.web_chunker.create_documents([page_str])
        chunSearch = Chroma.from_documents(web_chunks, self.web_sniptter_embed)
        relatedChunks = chunSearch.similarity_search(query_str, k=3)
        attended_content = '...'.join([chunk.page_content for chunk in relatedChunks])
        return attended_content


