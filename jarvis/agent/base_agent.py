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
<<<<<<< HEAD
                source_code = inspect.getsource(module) # wzm修改，通过自省获得文件源码
                tmp_obj = getattr(module, class_name)() #存储对象方式
                # 存储源码字符串
                self.action_lib.update({class_name:  source_code})# wzm修改，技能库存储文件源码而不是对象
                # self.action_lib.update({class_name: tmp_obj})
=======
                # get origin code
                source_code = inspect.getsource(module)
                # get class object
                tmp_obj = getattr(module, class_name)() 
                # save origin code
                self.action_lib.update({class_name: source_code})
                # save code description
>>>>>>> 4a892f6411471c671bbaf605ba10fc8b42db61f4
                self.action_lib_description.update({class_name: tmp_obj.description})
                
    # get class source code
    # def get_class_source_code(self, module, class_name):
    #     # 获取类对象
    #     tmp_obj = getattr(module, class_name)
    #     print(type(tmp_obj.description))
    #     self.action_lib_description.update({class_name: tmp_obj.description})
    #     # 获取类定义的源文件和行号
    #     source_file = inspect.getsourcefile(tmp_obj)
    #     source_lines, start_line = inspect.getsourcelines(tmp_obj)

    #     # 读取源文件
    #     with open(source_file, 'r') as file:
    #         lines = file.readlines()

    #     # 提取类的源代码
    #     class_code = ''.join(lines[start_line - 1: start_line - 1 + len(source_lines)])

    #     return class_code


if __name__ == '__main__':
    agent = BaseAgent()
    agent.init_action_lib()
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
    for k,v in agent.action_lib.items():
        toolName = k
        toolCode = v
        args = None
        # print(v())
        if(k == "python_interpreter"):
            args = "print('hello world')"
        res = myEnv.step(v+"\n"+"print({toolname}()({args}))".format(toolname=toolName,args=args))
        print(res.result)
        myEnv.reset()