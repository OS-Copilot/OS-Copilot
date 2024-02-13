__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
import json
import os

class ActionManager:
    def __init__(self, config_path=None, action_lib_dir=None):
        # actions: Store the mapping relationship between descriptions and code (associated through task names)
        self.actions = {}
        self.action_lib_dir = action_lib_dir
        with open(config_path) as f:
            config = json.load(f)
        with open(f"{self.action_lib_dir}/actions.json") as f2:
            self.actions = json.load(f2)
        self.vectordb_path = f"{action_lib_dir}/vectordb"

        if not os.path.exists(self.vectordb_path):
            os.makedirs(self.vectordb_path)
        # Utilize the Chroma database and employ OpenAI Embeddings for vectorization (defaul: text-embedding-ada-002)
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

    # View all the code in the code repository
    @property
    def programs(self):
        programs = ""
        for _, entry in self.actions.items():
            programs += f"{entry['code']}\n\n"
        return programs
    
    # Retrieve the descriptions of all actions
    @property
    def descriptions(self):
        descriptions = {}
        for action_name, entry in self.actions.items():
            descriptions.update({action_name: entry["description"]})
        return descriptions
    
    # Retrieve all action class names
    @property
    def action_names(self):
        return self.actions.keys()
    
    # View the code of a specific action
    def get_action_code(self, action_name):
        code = self.actions[action_name]['code']
        return code    

    # Add new task code
    def add_new_action(self, info):
        program_name = info["task_name"]
        program_code = info["code"]
        program_description = info["description"]
        print(
            f"\033[33m {program_name}:\n{program_description}\033[0m"
        )
        # If this task code already exists in the action library, delete it and rewrite
        if program_name in self.actions:
            print(f"\033[33mAction {program_name} already exists. Rewriting!\033[0m")
            self.vectordb._collection.delete(ids=[program_name])
        # Store the new task code in the vector database and the action dictionary
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
        # Store the new task code and description in the action library, and enter the mapping relationship into the dictionary
        with open(f"{self.action_lib_dir}/code/{program_name}.py", "w") as fa:
            fa.write(program_code)
        with open(f"{self.action_lib_dir}/action_description/{program_name}.txt", "w") as fb:
            fb.write(program_description)
        with open(f"{self.action_lib_dir}/actions.json", "w") as fc:
            json.dump(self.actions,fc,indent=4)
        self.vectordb.persist()

    # Check if there are relevant tools
    def exist_action(self, action):
        if action in self.action_names:
            return True
        return False

    # Retrieve related task names
    def retrieve_action_name(self, query, k=10):
        k = min(self.vectordb._collection.count(), k)
        if k == 0:
            return []
        print(f"\033[33mAction Manager retrieving for {k} Actions\033[0m")
        # Retrieve descriptions of the top k related tasks.
        docs_and_scores = self.vectordb.similarity_search_with_score(query, k=k)
        print(
            f"\033[33mAction Manager retrieved actions: "
            f"{', '.join([doc.metadata['name'] for doc, _ in docs_and_scores])}\033[0m"
        )
        action_name = []
        for doc, _ in docs_and_scores:
            action_name.append(doc.metadata["name"])
        return action_name
    
    # Return the task description based on the task name
    def retrieve_action_description(self, action_name):
        action_description = []
        for name in action_name:
            action_description.append(self.actions[name]["description"])
        return action_description    

    # Return the task code based on the task name
    def retrieve_action_code(self, action_name):
        action_code = []
        for name in action_name:
            action_code.append(self.actions[name]["code"])
        return action_code

    # Delete task-related information
    def delete_action(self, action):
        # Delete the task from the vector database
        if action in self.actions:
            self.vectordb._collection.delete(ids=[action])
            print(
            f"\033[33m delete {action} from vectordb successfully! \033[0m"
            )              
        # Delete the task from actions.json
        with open(f"{self.action_lib_dir}/actions.json", "r") as file:
            action_infos = json.load(file)
        if action in action_infos:
            del action_infos[action]
        with open(f"{self.action_lib_dir}/actions.json", "w") as file:
            json.dump(action_infos, file, indent=4)
            print(
            f"\033[33m delete {action} info from JSON successfully! \033[0m"
            )            
        # del code
        code_path = f"{self.action_lib_dir}/code/{action}.py"
        if os.path.exists(code_path):
            os.remove(code_path)
            print(
            f"\033[33m delete {action} code successfully! \033[0m"
            )
        # del description
        description_path = f"{self.action_lib_dir}/action_description/{action}.txt"
        if os.path.exists(description_path):
            os.remove(description_path)
            print(
            f"\033[33m delete {action} description txt successfully! \033[0m"
            )   
        # del args description
        args_path = f"{self.action_lib_dir}/args_description/{action}.txt"
        if os.path.exists(args_path):
            os.remove(args_path)
            print(
            f"\033[33m delete {action} args description txt successfully! \033[0m"
            )                
    

if __name__ == '__main__':
    actionManager = ActionManager(config_path="config.json", action_lib_dir="friday/action_lib")

    # Retrieval
    # res = actionManager.retrieve_action_name("Open the specified text file in the specified folder using the default text viewer on Ubuntu.")
    # print(res[0])

    # Delete
    # actionManager.delete_action("zip_files")

    # Add
    # code = ''
    # with open("temp.py", 'r') as file:
    #     code = file.read()
    # info = {
    #     "task_name" : "XXX",
    #     "code" : code,
    #     "description" : "XXX"
    # }
    # actionManager.add_new_action(info)