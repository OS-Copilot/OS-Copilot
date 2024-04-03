import sys

sys.dont_write_bytecode = True
from ..src import *

def screen() -> str:
    return Promise() \
        .then(xrandr)() \
        .then(grep)(" connected") \
        .then(cut)("-f1", "-d", " ")()
