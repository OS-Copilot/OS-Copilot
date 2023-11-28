import datetime
from typing import List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import sqlite3

router = APIRouter()


class SQLRequest(BaseModel):
    queries: List[str]


def execute_sql(queries: List[str]):
    conn = sqlite3.connect('./tasks/travel/database/travel.db')
    cursor = conn.cursor()

    results = []
    for query in queries:
        try:
            cursor.execute(query)
            results.append({
                "query": query,
                "result": cursor.fetchall(),
                "error": ""
            })
        except Exception as e:
            results.append({
                "query": query,
                "result": "",
                "error": str(e)
            })

    # Commit changes and close the connection to the database
    conn.commit()
    conn.close()

    return results


@router.post("/tools/database")
async def execute_sqlite(req: SQLRequest):
    print(f"{datetime.datetime.now()}:{req}")
    return execute_sql(req.queries)
