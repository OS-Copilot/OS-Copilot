import sys
import os

sys.dont_write_bytecode = True
from ..src import *

def create_dir(dir_path: str, new_dir_name: str) -> None:
    assert os.path.exists(dir_path)
    return mkdir(os.path.join(dir_path, new_dir_name))

def create_file(file_path: str, new_file_name: str) -> None:
    assert os.path.exists(file_path)
    return touch(os.path.join(file_path, new_file_name))

def download_file(url: str, file_name: str) -> None:
    return wget(url, "-O", file_name, "--no-check-certificate")

def copy(src_path: str, dst_path: str) -> None:
    assert os.path.exists(src_path)
    return cp(src_path, dst_path)  # cp a b

def move(src_path: str, dst_path: str) -> None:
    assert os.path.exists(src_path)
    return mv(src_path, dst_path)

def rename(file_path: str, new_file_name: str) -> None:
    assert os.path.exists(file_path)
    components = list(os.path.split(file_path))
    components[-1] = new_file_name
    dst = "/".join(components)
    return mv(file_path, dst)

def delete(path: str) -> None:
    assert os.path.exists(path)
    return rm("-rf", path)    
