from fastapi import APIRouter, HTTPException
from pydantic import BaseModel,Field
from typing import Optional
from .webpage2md import WebPage2MDTool
import tiktoken



router = APIRouter()

web2MdTool = WebPage2MDTool()

class TargetPageModel(BaseModel):
    url: str




@router.get("/tools/markdown/web2md")
async def get_web_md(item: TargetPageModel):
    result = {"markdown": ""}
    try:
        markdown_text = web2MdTool.get_web_md(item.url)
        result["markdown"] = markdown_text
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    return result