import os
import sys
import glob
from jarvis.action.base_action import BaseAction
import importlib
from typing import Optional

class BaseAgent:
    """
    BaseAgent is the base class of all agents.
    """
    def __init__(self, config_path=None):
        self.llm = None
        self.environment = None
        self.action_lib = {}
        self.action_lib_description = {}
        self.action = None
        self.init_action_lib()
    #
    # def from_config(self, config_path=None):
    #     raise NotImplementedError

    def init_action_lib(self, path=None, attribute_name='_description'):
        if not path:
            path = os.path.abspath(os.path.join(os.getcwd(), "..", "action_lib"))
        sys.path.append(path)
        files = glob.glob(path + "/*.py")
        for file in files:
            if file.endswith('.py') and "__init__" not in file:
                class_name = file[:-3].split('/')[-1]  # 去除.py后缀，获取类名
                module = importlib.import_module(class_name)
                tmp_obj = getattr(module, class_name)()
                self.action_lib.update({class_name: tmp_obj._command})
                self.action_lib_description.update({class_name: tmp_obj.description})


if __name__ == '__main__':
    a = BaseAgent()
    a.init_action_lib()
    for k,v in a.action_lib.items():
        print(k)
        print(v)