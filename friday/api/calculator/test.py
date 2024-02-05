import requests
import json

# 测试加法
expression = "((46210 - 8*9068) / (2 - x))"
response = requests.post(
    'http://127.0.0.1:8079/tools/calculator',
    json={'expression': expression}
)
print(response.json())