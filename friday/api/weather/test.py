# test_weather_api.py

import requests

def test_query_weather():
    base_url = "http://127.0.0.1:8079"
    date = "2023-07-01"
    city = "Beijing"

    # 发送GET请求到/weather/query端点
    response = requests.get(f"{base_url}/weather/query", params={"date": date, "city": city})

    # 检查响应是否成功
    if response.status_code == 200:
        print("Test Passed")
        print("Response JSON:", response.json())
    else:
        print("Test Failed")
        print("Response Status Code:", response.status_code)
        print("Response JSON:", response.json())

if __name__ == "__main__":
    test_query_weather()