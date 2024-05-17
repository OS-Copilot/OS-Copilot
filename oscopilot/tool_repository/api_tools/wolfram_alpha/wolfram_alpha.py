from fastapi import APIRouter
import wolframalpha
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv


load_dotenv(dotenv_path='.env', override=True)

WOLFRAMALPHA_APP_ID = os.getenv('WOLFRAMALPHA_APP_ID')

class QueryItem(BaseModel):
    query: str

router = APIRouter()

app_id = WOLFRAMALPHA_APP_ID
client = wolframalpha.Client(app_id)

@router.post("/tools/wolframalpha")
async def wolframalpha_query(item: QueryItem):
    res = client.query(item.query)

    # Handle the query result
    if res['@success'] == 'false':
        return {"result": "Query failed"}
    else:
        # Return the first result text
        result = next(res.results).text
        return {"result": result}