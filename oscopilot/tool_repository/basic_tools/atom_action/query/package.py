import sys

sys.dont_write_bytecode = True
from ..src import *

def is_installed(package: str) -> str:
    return Promise() \
        .then(apt)("list") \
        .then(grep)(f"{package}/")()
