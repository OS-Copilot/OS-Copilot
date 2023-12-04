
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
import json
import os
import glob
import importlib
import inspect
import sys
'''
    Made by @wzm
    使用Chroma向量数据库进行任务代码的检索、存储和更新
'''

class ActionManager:
    def __init__(self
                 , config_path=None
                 , action_lib_dir=None
                 , retrieval_top_k=1):
        # actions: 存放描述和代码的映射关系(通过任务名做关联)
        self.actions = {}
        self.action_lib_dir = action_lib_dir
        self.retrieval_top_k = retrieval_top_k
        with open(config_path) as f:
            config = json.load(f)
        with open(f"{self.action_lib_dir}/actions.json") as f2:
            self.actions = json.load(f2)
        self.vectordb_path = f"{action_lib_dir}/vectordb";
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
        for action_name, entry in self.actions.items():
            programs += f"{entry['code']}\n\n"
        return programs
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
        # with open(f"{self.action_lib_dir}/code/{program_name}.py", "w") as fa:
        #     fa.write(program_code)
        # with open(f"{self.action_lib_dir}/description/{program_name}.txt", "w") as fb:
        #     fb.write(program_description)
        with open(f"{self.action_lib_dir}/actions.json", "w") as fc:
            json.dump(self.actions,fc,indent=4)
        self.vectordb.persist()
    # 检索相关任务代码
    def retrieve_actions(self, query):
        k = min(self.vectordb._collection.count(), self.retrieval_top_k)
        if k == 0:
            return []
        print(f"\033[33mAction Manager retrieving for {k} Actions\033[0m")
        # 检索top k相关的任务描述
        docs_and_scores = self.vectordb.similarity_search_with_score(query, k=k)
        print(
            f"\033[33mAction Manager retrieved actions: "
            f"{', '.join([doc.metadata['name'] for doc, _ in docs_and_scores])}\033[0m"
        )
        actions = []
        for doc, _ in docs_and_scores:
            actions.append(self.actions[doc.metadata["name"]]["code"])
        return actions

    
# demo
actionManager = ActionManager(config_path="../../examples/config.json", action_lib_dir="../action_lib", retrieval_top_k=2)
sys.path.append('../action_lib')
# # 添加所有任务代码
# files = glob.glob("../action_lib" + "/*.py")
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
res = actionManager.retrieve_actions("set a 10s timer")
print(res[0])

