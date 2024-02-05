import sys

sys.dont_write_bytecode = True
from ..src import *

def exec_python(file_path: str) -> None:
    return python(file_path)

def open_editor(file_path: str) -> None:
    return gedit(file_path)

def open_vscode(path: str) -> None:
    return code(path)




