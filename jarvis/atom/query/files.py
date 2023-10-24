import sys

sys.dont_write_bytecode = True
from ..src import *

def dir_list(dir_path: str) -> str:
    return ls(dir_path)

def dir_tree(dir_path: str) -> str:
    return tree(dir_path)
