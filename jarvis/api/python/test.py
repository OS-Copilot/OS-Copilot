import requests
import json

code = """
import heapq as hq\r\nfrom collections import Counter\r\n\r\ndef func(lists, k):\r\n    nums = []\r\n    for lst in lists:\r\n        nums.extend(lst)\r\n    count = Counter(nums)\r\n    top_k = hq.nlargest(k, count, key=count.get)\r\n    return top_k\nassert func([[1, 2, 6], [1, 3, 4, 5, 7, 8], [1, 3, 5, 6, 8, 9], [2, 5, 7, 11], [1, 4, 7, 8, 12]],3)==[5, 7, 1]\nassert func([[1, 2, 6], [1, 3, 4, 5, 7, 8], [1, 3, 5, 6, 8, 9], [2, 5, 7, 11], [1, 4, 7, 8, 12]],1)==[1]\nassert func([[1, 2, 6], [1, 3, 4, 5, 7, 8], [1, 3, 5, 6, 8, 9], [2, 5, 7, 11], [1, 4, 7, 8, 12]],5)==[6, 5, 7, 8, 1]\n
"""
code="""
print('hello world')"""
response = requests.post(
    'http://127.0.0.1:8079/tools/python',
    json={'code': code}
)

print(response.json())