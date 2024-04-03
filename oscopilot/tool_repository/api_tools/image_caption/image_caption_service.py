from fastapi import APIRouter, HTTPException,UploadFile,File,Form, Depends
from pydantic import BaseModel,Field
from typing import Optional
from .gpt4v_caption import ImageCaptionTool
import base64

router = APIRouter()

image_caption_api = ImageCaptionTool()


# class CaptionQueryItem(BaseModel):
#     query: Optional[str] = "What's in this image?"
#     url: Optional[str] = None
#     image_file: Optional[UploadFile] = File(None)

async def caption_parameters(query: Optional[str] = Form("What's in this image?"),url: Optional[str] = Form(None),image_file: Optional[UploadFile] = File(None)):
    return {"query":query,"url":url,"image_file":image_file}

@router.post("/tools/image_caption", summary="When the task is to question and answer based on local picture, you have to use the Image Caption tool, who can directly analyze picture to answer question and complete task. For local images you want to understand, you need to only give the image_file without url. It is crucial to provide the 'query' parameter, and its value must be the full content of the task itself.")
async def image_search(item: dict = Depends(caption_parameters)):
    try:
        if(item["query"] == None):
            item["query"] = "What's in this image?"
        if(item["url"] == None and item["image_file"] == None):
            return {"error":"Invalid picture"}
        image_url=""
        if(item["url"] != None and item["image_file"] == None):
            image_url = item["url"]
        elif(item["image_file"] != None):
            base64Img = base64.b64encode(await item["image_file"].read()).decode('utf-8')
            image_url = f"data:image/jpeg;base64,{base64Img}"
        caption = image_caption_api.caption(url=image_url,query=item["query"])
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"caption":caption}

