from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from .bing_api import BingAPI

router = APIRouter()

bing_api = BingAPI('885e62a126554fb390af88ae31d2c8ff')

class QueryItem(BaseModel):
    query: str

class PageItem(BaseModel):
    url: str

@router.get("/tools/bing/search")
async def bing_search(item: QueryItem):
    try:
        search_results = bing_api.search(item.query)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    return search_results

@router.get("/tools/bing/load_page")
async def load_page(item: PageItem):
    try:
        page_loaded, page_detail = bing_api.load_page(item.url)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    if not page_loaded:
        raise HTTPException(status_code=500, detail=page_detail)
    return {"page_content": page_detail}