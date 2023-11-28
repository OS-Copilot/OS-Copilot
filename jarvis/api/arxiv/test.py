import requests

response = requests.get(
    'http://127.0.0.1:8079/tools/arxiv',
    json={'query': 'OpenICL'}
)

print(response.json())