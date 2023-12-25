import requests

response = requests.get(
    'http://10.241.41.203:8079/tools/arxiv',
    json={'query': 'autogen'}
)

print(response.json())