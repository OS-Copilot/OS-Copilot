from fastapi import APIRouter, HTTPException
from pydantic import BaseModel,Field
from typing import Optional
from .bing_api import BingAPI
from .bing_api_v2 import BingAPIV2
import tiktoken

# 计算网页内容对gpt4来说的token数，如果token太多就用3.5做摘要或者用向量数据库检索最相关的片段
def num_tokens_from_string(string: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model('gpt-4-1106-preview')
    num_tokens = len(encoding.encode(string))
    return num_tokens

router = APIRouter()

bing_api = BingAPI('885e62a126554fb390af88ae31d2c8ff')
bing_api_v2 = BingAPIV2()

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

@router.get("/tools/bing/searchv2")
async def bing_search_v2(item: QueryItemV2):
    try:
        if item.top_k == None:
            item.top_k = 5
        search_results = bing_api_v2.search(item.query,item.top_k)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    return search_results

@router.get("/tools/bing/load_pagev2")
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