from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from simpleeval import simple_eval, SimpleEval

router = APIRouter()

class Expression(BaseModel):
    expression: str


@router.post("/tools/calculator")
def evaluate(expression: Expression):
    try:
        s = SimpleEval()
        result = s.eval(expression.expression)
        return {"result": str(result), "error": None}
    except Exception as e:
        return {"result": None, "error": str(e)}
