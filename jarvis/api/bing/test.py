import requests

response = requests.get(
    'http://127.0.0.1:8079/tools/bing/search',
    json={'query': 'Python'}
)
print(response.json())

response = requests.get(
    'http://127.0.0.1:8079/tools/bing/load_page',
    json={'url': 'https://www.python.org/'}
)
print(response.json())