import os
import sys
import glob
from jarvis.action.base_action import BaseAction
import importlib
from typing import Optional
import inspect
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
            path = os.path.abspath(os.path.join(__file__, "..", "..", "action_lib"))
        sys.path.append(path)
        files = glob.glob(path + "/*.py")
        for file in files:
            if file.endswith('.py') and "__init__" not in file:
                class_name = file[:-3].split('/')[-1]  # 去除.py后缀，获取类名
                module = importlib.import_module(class_name)
                source_code = inspect.getsource(module) # wzm修改，通过自省获得文件源码
                tmp_obj = getattr(module, class_name)() #存储对象方式
                # 存储源码字符串
                self.action_lib.update({class_name:  source_code })# wzm修改，技能库存储文件源码而不是对象
                # self.action_lib.update({class_name: tmp_obj})
                self.action_lib_description.update({class_name: tmp_obj.description})

   
if __name__ == '__main__':
    a = BaseAgent()
    a.init_action_lib()
    from jarvis.enviroment.py_env import PythonEnv
    myEnv = PythonEnv()
    # toolName = "execute_sql"
    # res = myEnv.step(a.action_lib['{toolname}'.format(toolname=toolName)]+"\n"+"print({toolname}()())".format(toolname=toolName))
    # print(res.result)
    # print(a.action_lib_description)
    # res = a.action_lib["execute_sql"]()
    # print(res)
    # print(a.action_lib)
    # print(a.action_lib_description)
    for k,v in a.action_lib.items():
        toolName = k
        toolCode = v
        args = None
        # print(v())
        if(k == "python_interpreter"):
            args = "print('hello world')"
        res = myEnv.step(v+"\n"+"print({toolname}()({args}))".format(toolname=toolName,args=args))
        print(res.result)
        myEnv.reset()