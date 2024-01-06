from fastapi import APIRouter, HTTPException, File, UploadFile,Depends
from pydantic import BaseModel,Field
from typing import Optional
from .audio2text import Audio2TextTool
import io
import os
import shutil
router = APIRouter()

whisper_api = Audio2TextTool()


class AudioTextQueryItem(BaseModel):
    file: UploadFile = File(...)



@router.post("/tools/audio2text")
async def audio2text(item: AudioTextQueryItem = Depends()):
    try:
        # 创建一个临时文件来保存上传的音频
        with open(item.file.filename, "wb") as buffer:
            shutil.copyfileobj(item.file.file, buffer)
        with open(item.file.filename, "rb") as audio:
            caption = whisper_api.caption(audio_file=audio)
        # 清理临时文件
        os.remove(item.file.filename)
        return {"text": caption}
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

