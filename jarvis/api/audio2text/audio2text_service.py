from fastapi import APIRouter, HTTPException, File, UploadFile,Depends
from pydantic import BaseModel,Field
from typing import Optional
from .audio2text import Audio2TextTool


router = APIRouter()

whisper_api = Audio2TextTool()


class AudioTextQueryItem(BaseModel):
    file: UploadFile = File(...)



@router.post("/tools/audio2text")
async def audio2text(item: AudioTextQueryItem = Depends()):
    try:
        #  # 读取上传的文件
        # contents = await item.file.read()
        caption = whisper_api.caption(audio_file=item.file)
        return {"text": caption}
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

