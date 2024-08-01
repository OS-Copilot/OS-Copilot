from fastapi import APIRouter, HTTPException
from pydantic import BaseModel,Field
from typing import Optional
# from .bing_api import BingAPI
from .bing_api_v2 import BingAPIV2
from .image_search_api import ImageSearchAPI
import tiktoken
import os
from dotenv import load_dotenv


load_dotenv(dotenv_path='.env', override=True)

BING_API = os.getenv('BING_SUBSCRIPTION_KEY')  # set bing API


# Calculate the number of tokens in the webpage content for GPT-4. If there are too many tokens, use GPT-3.5 for summarization or search the vector database for the most relevant segment.
def num_tokens_from_string(string: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model('gpt-4-1106-preview')
    num_tokens = len(encoding.encode(string))
    return num_tokens

router = APIRouter()

# bing_api = BingAPI(BING_API) 
bing_api_v2 = BingAPIV2()
image_search_api = ImageSearchAPI(BING_API) 

# class QueryItem(BaseModel):
#     query: str

# class PageItem(BaseModel):
#     url: str

class QueryItemV2(BaseModel):
    query: str
    top_k: Optional[int] = Field(None)
class PageItemV2(BaseModel):
    url: str
    query: Optional[str] = Field(None)

# @router.get("/tools/bing/search")
# async def bing_search(item: QueryItem):
#     try:
#         search_results = bing_api.search(item.query)
#     except RuntimeError as e:
#         raise HTTPException(status_code=500, detail=str(e))
#     return search_results

# @router.get("/tools/bing/load_page")
# async def load_page(item: PageItem):
#     try:
#         page_loaded, page_detail = bing_api.load_page(item.url)
#     except RuntimeError as e:
#         raise HTTPException(status_code=500, detail=str(e))
#     if not page_loaded:
#         raise HTTPException(status_code=500, detail=page_detail)
#     return {"page_content": page_detail}

@router.get("/tools/bing/image_search", summary="Searches for images related to the provided keywords using the Bing Image Search API. It allows specifying the number of images to return (top_k) and retries the search up to a specified number of times (max_retry) in case of failures. The search is performed with a moderate safe search filter and is intended for use within an environments that requires image search capabilities. The function returns a list of images, including their names, URLs, and thumbnail information. If the search fails after the maximum number of retries, it raises a runtime error.")
async def image_search(item: QueryItemV2):
    try:
        if item.top_k == None:
            item.top_k = 10
        search_results = image_search_api.search_image(item.query,item.top_k)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    return search_results

@router.get("/tools/bing/searchv2", summary="Execute Bing Search - returns top web snippets related to the query. Avoid using complex filters like 'site:'. For detailed page content, further use the web browser tool.")
async def bing_search_v2(item: QueryItemV2):
    try:
        if item.top_k == None:
            item.top_k = 5
        search_results = bing_api_v2.search(item.query,item.top_k)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    return search_results

@router.get("/tools/bing/load_pagev2", summary="Web browser tool for detailed content retrieval and specific information extraction from a target URL.In the case of Wikipedia, the number of tokens on such pages is often too large to load the entire page, so the 'query' parameter must be given to perform a similarity query to find the most relevant pieces of content. The 'query' parameter should be assigned with your task description to find the most relevant content of the web page.It is important that your 'query' must retain enough details about the task, such as time, location, quantity, and other information, to ensure that the results obtained are accurate enough.")
async def load_page_v2(item: PageItemV2):
    result = {"page_content": ""}
    try:
        raw_page_content = bing_api_v2.load_page(item.url)
        page_token_num = num_tokens_from_string(raw_page_content)
        if(page_token_num <= 4096):
            result = {"page_content": raw_page_content}
        else:
            if item.query == None:
                summarized_page_content = bing_api_v2.summarize_loaded_page(raw_page_content)
                result = {"page_content": summarized_page_content}
            else:
                attended_content = bing_api_v2.attended_loaded_page(raw_page_content,item.query)
                result = {"page_content": attended_content}
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    return result