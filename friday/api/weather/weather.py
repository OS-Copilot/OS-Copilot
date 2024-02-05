# api/weather/weather.py
from fastapi import APIRouter, HTTPException, Query
import sqlite3

router = APIRouter()

@router.get("/weather/query")  # 注意这里改为GET请求
def query_weather(date: str, city: str):  # 使用Query参数
    try:
        conn = sqlite3.connect('./database/weather.db')
        c = conn.cursor()
        c.execute("SELECT max_temp, min_temp, weather FROM weather WHERE city=? AND date=?", (city, date))
        row = c.fetchone()
        conn.close()

        if row:
            result=f'{date}, {city}: {row[2]}, {row[1]}-{row[0]} ℃'
            return {"result": str(result), "error": None}
        else:
            {"result": '', "error": 'data not found'}

    except Exception as e:
        print(e)
        return {"result": '', "error": 'not found'}
