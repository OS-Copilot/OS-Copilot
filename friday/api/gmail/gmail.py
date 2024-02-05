import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request as google_request
from googleapiclient.discovery import build
import base64
from email.mime.text import MIMEText
import pickle

SCOPES = ['https://www.googleapis.com/auth/gmail.send', 'https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/calendar']


def get_service():
    creds = None
    # 尝试从 "token.pickle" 文件中加载凭据
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if creds and not creds.valid:
        if creds.expired and creds.refresh_token:
            creds.refresh(google_request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            './.auth/calendar.json', SCOPES)
        creds = flow.run_local_server(port=0)
    service = build('gmail', 'v1', credentials=creds)
    return service


def send_email(service, from_email, to_email, subject, content):
    message = MIMEText(content)
    message['to'] = to_email
    message['from'] = from_email
    message['subject'] = subject
    raw_message = base64.urlsafe_b64encode(message.as_string().encode("utf-8"))
    message = {'raw': raw_message.decode("utf-8")}
    message = (service.users().messages().send(userId='me', body=message).execute())


from fastapi import APIRouter
import json
import base64
from email.mime.text import MIMEText
from pydantic import BaseModel

router = APIRouter()


class EmailSchema(BaseModel):
    from_email: str
    to_email: str
    subject: str
    content: str


@router.post("/gmail/send")
def send_test_email(email: EmailSchema):
    try:
        service = get_service()
        send_email(service, email.from_email, email.to_email, email.subject, email.content)  # 注意这里从email对象中取字段
        return {"result": "Email sent successfully", "error": None}
    except Exception as e:
        return {"result": None, "error": str(e)}


# token.pickle文件包含了与特定Gmail账户关联的访问令牌
@router.get("/gmail/list")
def list_recent_emails():
    try:
        service = get_service()
        results = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=10).execute()
        messages = results.get('messages', [])
        emails = []
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            email_data = msg['payload']['headers']
            for values in email_data:
                name = values['name']
                if name == 'From':
                    from_name = values['value']
                    subject = msg['snippet']
                    emails.append({"from": from_name, "subject": subject})
        return {"emails": emails, "error": None}
    except Exception as e:
        return {"emails": None, "error": str(e)}
