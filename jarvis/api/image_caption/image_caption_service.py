from fastapi import APIRouter, HTTPException
from pydantic import BaseModel,Field
from typing import Optional
from .gpt4v_caption import ImageCaptionTool


router = APIRouter()

image_caption_api = ImageCaptionTool()


class CaptionQueryItem(BaseModel):
    query: Optional[str] = "What's in this image?"
    url: str



@router.get("/tools/image_caption")
async def image_search(item: CaptionQueryItem):
    try:
        if(item.query == None):
            item.query = "What's in this image?"
        if(item.url == None):
            return "Invalid picture url"
        caption = image_caption_api.caption(url=item.url,query=item.query)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    return caption

