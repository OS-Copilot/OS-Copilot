# 开启Google Calendar API并下载凭据: 访问Google Cloud Console，创建一个新的项目并启用Google Calendar API。下载生成的credentials.json文件。
import os

from fastapi import APIRouter
from pydantic import BaseModel, Field
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request as google_request
from googleapiclient.discovery import build
import pickle

# 如果修改了SCOPES，请删除文件token.pickle。
SCOPES = ['https://www.googleapis.com/auth/gmail.send','https://www.googleapis.com/auth/gmail.readonly','https://www.googleapis.com/auth/calendar']



def get_service():
    creds = None
    # 尝试从 "token.pickle" 文件中加载凭据
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # 如果凭据无效，重新获取
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(google_request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                './.auth/calendar.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # 保存新的凭据到 "token.pickle" 文件
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service
router = APIRouter()


class CalendarEvent(BaseModel):
    summary: str
    location: str
    description: str
    start: dict = Field(..., example={"dateTime": "2023-07-31T15:00:00", "timeZone": "Asia/Shanghai"})
    end: dict = Field(..., example={"dateTime": "2023-07-31T16:00:00", "timeZone": "Asia/Shanghai"})


@router.post("/calendar/insert_event")
def insert_event(event: CalendarEvent):
    try:
        # 这里你可以调用Google Calendar API
        service = get_service()  # 从你原来的代码获取service
        inserted_event = service.events().insert(calendarId='primary', body=event.dict()).execute()
        return {"result": f'Event created: {inserted_event["htmlLink"]}', "error": None}
    except Exception as e:
        return {"result": None, "error": str(e)}
