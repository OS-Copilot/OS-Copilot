from fastapi import APIRouter
from pydantic import BaseModel
import subprocess

router = APIRouter()

class ShellCommandModel(BaseModel):
    command: str

class ShellCommandResultModel(BaseModel):
    stdout: str
    stderr: str

@router.post("/tools/shell", response_model=ShellCommandResultModel)
async def execute_shell_command(command: ShellCommandModel):
    result = subprocess.run(command.command, capture_output=True, shell=True, text=True)
    return ShellCommandResultModel(stdout=result.stdout, stderr=result.stderr)
