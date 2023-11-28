import requests
import json

# 用于测试的日历事件
test_event = {
    "summary": "NLUI会议",
    "location": "上海",
    "description": "这是一个关于NLUI的会议",
    "start": {
        "dateTime": "2023-08-28T10:30:00",
        "timeZone": "Asia/Shanghai"
    },
    "end": {
        "dateTime": "2023-08-28T11:30:00",  # 假设会议时长为1小时
        "timeZone": "Asia/Shanghai"
    }
}

# 向API发送请求
response = requests.post("http://127.0.0.1:8079/calendar/insert_event", json=test_event)

# 解析响应
if response.status_code == 200:
    data = response.json()
    print(data)