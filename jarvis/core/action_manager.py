
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
import json
import os
import glob
import importlib
import inspect
import sys
'''
    Made by @wzm & dzc
    使用Chroma向量数据库进行任务代码的检索、存储和更新
'''

class ActionManager:
    def __init__(self, config_path=None, action_lib_dir=None):
        # actions: 存放描述和代码的映射关系(通过任务名做关联)
        self.actions = {}
        self.action_lib_dir = action_lib_dir
        with open(config_path) as f:
            config = json.load(f)
        with open(f"{self.action_lib_dir}/actions.json") as f2:
            self.actions = json.load(f2)
        self.vectordb_path = f"{action_lib_dir}/vectordb"
        # 没有向量数据库的存储路径就创一个
        if not os.path.exists(self.vectordb_path):
            os.makedirs(self.vectordb_path)
        # 使用Chroma数据库，使用OpenAIEmbeddings进行向量化(默认是text-embedding-ada-002)
        self.vectordb = Chroma(
            collection_name="action_vectordb",
            embedding_function=OpenAIEmbeddings(
                openai_api_key=config['OPENAI_API_KEY'],
                openai_organization=config['OPENAI_ORGANIZATION'],
            ),
            persist_directory=self.vectordb_path,
        )
        assert self.vectordb._collection.count() == len(self.actions), (
            f"Action Manager's vectordb is not synced with actions.json.\n"
            f"There are {self.vectordb._collection.count()} actions in vectordb but {len(self.actions)} actions in actions.json.\n"
        )

    # 查看代码库中所有的代码
    @property
    def programs(self):
        programs = ""
        for _, entry in self.actions.items():
            programs += f"{entry['code']}\n\n"
        return programs
    
    # 获取所有action的description 
    @property
    def descriptions(self):
        descriptions = {}
        for action_name, entry in self.actions.items():
            descriptions.update({action_name: entry["description"]})
        return descriptions
    
    # 获取所有的action类名
    @property
    def action_names(self):
        return self.actions.keys()
    
    # 查看某个动作的代码
    def get_action_code(self, action_name):
        code = self.actions[action_name]['code']
        return code    

    # 添加新的任务代码
    def add_new_action(self, info):
        program_name = info["task_name"]
        program_code = info["code"]
        program_description = info["description"]
        print(
            f"\033[33m {program_name}:\n{program_description}\033[0m"
        )
        # 如果action library中已经存在这个任务代码，就删了重写
        if program_name in self.actions:
            print(f"\033[33mAction {program_name} already exists. Rewriting!\033[0m")
            self.vectordb._collection.delete(ids=[program_name])
        # 将新的任务代码存入向量数据库以及action字典
        self.vectordb.add_texts(
            texts=[program_description],
            ids=[program_name],
            metadatas=[{"name": program_name}],
        )
        self.actions[program_name] = {
            "code": program_code,
            "description": program_description,
        }
        assert self.vectordb._collection.count() == len(
            self.actions
        ), "vectordb is not synced with actions.json"
        # 将新的任务代码、描述存入action library，并将映射关系存入字典
        with open(f"{self.action_lib_dir}/code/{program_name}.py", "w") as fa:
            fa.write(program_code)
        with open(f"{self.action_lib_dir}/action_description/{program_name}.txt", "w") as fb:
            fb.write(program_description)
        with open(f"{self.action_lib_dir}/actions.json", "w") as fc:
            json.dump(self.actions,fc,indent=4)
        self.vectordb.persist()
    
    # 检索相关任务代码
    # def retrieve_action_code(self, query):
    #     k = min(self.vectordb._collection.count(), self.retrieval_top_k)
    #     if k == 0:
    #         return []
    #     print(f"\033[33mAction Manager retrieving for {k} Actions\033[0m")
    #     # 检索top k相关的任务描述
    #     docs_and_scores = self.vectordb.similarity_search_with_score(query, k=k)
    #     print(
    #         f"\033[33mAction Manager retrieved actions: "
    #         f"{', '.join([doc.metadata['name'] for doc, _ in docs_and_scores])}\033[0m"
    #     )
    #     action_code = []
    #     for doc, _ in docs_and_scores:
    #         action_code.append(self.actions[doc.metadata["name"]]["code"])
    #     return action_code
    # 检查是否有相关工具
    def exist_action(self, action):
        if action in self.action_names:
            return True
        return False


    # 检索相关任务名称
    def retrieve_action_name(self, query, k=10):
        k = min(self.vectordb._collection.count(), k)
        if k == 0:
            return []
        print(f"\033[33mAction Manager retrieving for {k} Actions\033[0m")
        # 检索top k相关的任务描述
        docs_and_scores = self.vectordb.similarity_search_with_score(query, k=k)
        print(
            f"\033[33mAction Manager retrieved actions: "
            f"{', '.join([doc.metadata['name'] for doc, _ in docs_and_scores])}\033[0m"
        )
        action_name = []
        for doc, _ in docs_and_scores:
            action_name.append(doc.metadata["name"])
        return action_name
    
    # 根据任务名称返回任务描述
    def retrieve_action_description(self, action_name):
        action_description = []
        for name in action_name:
            action_description.append(self.actions[name]["description"])
        return action_description    

    # 根据任务名称返回任务代码
    def retrieve_action_code(self, action_name):
        action_code = []
        for name in action_name:
            action_code.append(self.actions[name]["code"])
        return action_code

    # 删除任务相关信息
    def delete_action(self, action):
        # 从向量数据库中删除任务
        if action in self.actions:
            self.vectordb._collection.delete(ids=[action])
            print(
            f"\033[33m delete {action} from vectordb successfully! \033[0m"
            )              
        # 从actions.json中删除任务
        with open(f"{self.action_lib_dir}/actions.json", "r") as file:
            action_infos = json.load(file)
        if action in action_infos:
            del action_infos[action]
        with open(f"{self.action_lib_dir}/actions.json", "w") as file:
            json.dump(action_infos, file, indent=4)
            print(
            f"\033[33m delete {action} info from JSON successfully! \033[0m"
            )            
        # 删除code
        code_path = f"{self.action_lib_dir}/code/{action}.py"
        if os.path.exists(code_path):
            os.remove(code_path)
            print(
            f"\033[33m delete {action} code successfully! \033[0m"
            )
        # 删除description
        description_path = f"{self.action_lib_dir}/action_description/{action}.txt"
        if os.path.exists(description_path):
            os.remove(description_path)
            print(
            f"\033[33m delete {action} description txt successfully! \033[0m"
            )   
        # 删除args description
        args_path = f"{self.action_lib_dir}/args_description/{action}.txt"
        if os.path.exists(args_path):
            os.remove(args_path)
            print(
            f"\033[33m delete {action} args description txt successfully! \033[0m"
            )                
    

if __name__ == '__main__':
    actionManager = ActionManager(config_path="../../examples/config.json", action_lib_dir="../action_lib")
    # action_list = json.dumps(actionManager.descriptions)
    # print(action_list)
    # sys.path.append('../action_lib/code')
    # # 添加所有任务代码
    # files = glob.glob("../action_lib/code" + "/*.py")
    # for file in files:
    #     if file.endswith('.py') and "__init__" not in file:
    #         class_name = file[:-3].split('/')[-1]  # 去除.py后缀，获取类名
    #         print(f"当前类:{class_name}")
    #         module = importlib.import_module(class_name)
    #         # get origin code
    #         source_code = inspect.getsource(module)
    #         # get class object
    #         tmp_obj = getattr(module, class_name)() 
    #         # 报错到向量数据库和字典
    #         actionManager.add_new_action({
    #             "task_name": class_name,
    #             "code": source_code,
    #             "description": tmp_obj.description
    #         })
    # 检索
    # res = actionManager.retrieve_action_name("Open the specified text file in the specified folder using the default text viewer on Ubuntu.")
    # print(res[0])

    # 删除
    # actionManager.delete_action("implement_newtons_method")
    # actionManager.delete_action("zip_files")
    # print(actionManager.action_code('zip_files'))

    # 手动添加action
    # code = ''
    # with open("/home/heroding/桌面/Jarvis/working_dir/code/temp.py", 'r') as file:
    #     code = file.read()

    # info = {
    #     "task_name" : "implement_newtons_method",
    #     "code" : code,
    #     "description" : "Implement Newton's Method to find a root of the function f(x)."
    # }

    # actionManager.add_new_action(info)