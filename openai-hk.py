import requests
import json

url = "https://api.openai-hk.com/v1/chat/completions"

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer hk-y7oqw81000007081956c9eae69ef0ec39fb67374833ee3f4"
}

data = {
    "max_tokens": 1200,
    "model": "gpt-4",
    "temperature": 0.8,
    "top_p": 1,
    "presence_penalty": 1,
    "messages": [
        {
            "role": "system",
            "content": "You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as possible."
        },
        {
            "role": "user",
            "content": "帮我写一个AppleScript代码，在macos上定一个20分钟的闹钟。"
        }
    ]
}

response = requests.post(url, headers=headers, data=json.dumps(data).encode('utf-8') )
result = response.content.decode("utf-8")

print(result)