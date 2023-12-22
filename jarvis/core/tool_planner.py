import requests
import json
import os
from langchain.utilities import BingSearchAPIWrapper
from jarvis.action.get_os_version import get_os_version, check_os_version
from jarvis.core.llms import OpenAI

sys_prompt = '''
You are a helpful assistant that can answer the user's questions with the help of tools.You are provided with the following tools:
Tools:
1. {{
    "tool_name": "bing_search",
    "description": "You can use this tool to search top 10 relevant web pages' link and very short description for the given query keywords.You sometimes need to use web browser to get detailed information of some page"
    "path": "/api/tools/bing/search",
    "method": "get",
    "params": [
        {{
            "name": "query",
            "in":"query",
            "type": "string",
            "description": "the query keywords for bing search"
        }},
        
    ],
    
}}
2. {{
    "tool_name": "web_browser",
    "description": "You can use this tool to browser the detail content of the web page given its url"
    "path": "/api/tools/bing/search",
    "method": "get",
    "params": [
        {{
            "name": "query",
            "in":"query",
            "type": "string",
            "description": "the query keywords for bing search"
        }},
        
    ],
    
}}
You need to decide whether which tools to use to solve the question asked by user.
Remember if you can make sure the answer you give by your own knowledge is completely accurate, don't use any tools. Only use the tools provided to you if you lack some external knowledge to give a factual answer. You can even use multiple tools or use the same tool multiple times if necessary.
You should give me a plan list to tell me how to use the tools to solve the question,the response format should just like:
eg. To solve the question "How many studio albums were published by Mercedes Sosa between 2000 and 2009 (included)?"
1. <tool>/api/tools/bing/search?query=Mercedes Sosa</tool>
2. <tool>/api/tools/bing/load_page?url=https://en.wikipedia.org/wiki/Mercedes_Sosa</tool>
If you think there is no need to use tools, you can just respond:
There is no need to use tools.
Now,you can start to solve the question,give me your plans:
{question}
'''

os.environ["BING_SUBSCRIPTION_KEY"] = "885e62a126554fb390af88ae31d2c8ff"
os.environ["BING_SEARCH_URL"] = "https://api.bing.microsoft.com/v7.0/search"
# search = BingSearchAPIWrapper()
 
# res = search.results("https://zhuanlan.zhihu.com/p/623421034 summary",10)
class ToolPlanner():
    """
    SkillCreator is used to generate new skills and store them in the action_lib.
    """
    def __init__(self, config_path=None) -> None:
        super().__init__()
        self.llm = OpenAI(config_path)
        self.system_version = get_os_version()
        try:
            check_os_version(self.system_version)
        except ValueError as e:
            print(e)
        # self.mac_systom_prompts = 

    def format_message(self, task):
        self.prompt = sys_prompt.format(question=task)
        # self.prompt = ""
        print(self.prompt)
        self.message = [
            {"role": "system", "content": self.prompt},
            {"role": "user", "content": task},
        ]
        return self.llm.chat(self.message)
q = '''
What writer is quoted by Merriam-Webster for the Word of the Day from June 27, 2022?
'''
res = ToolPlanner("../../examples/config.json").format_message(q)        
print(res)
 
 