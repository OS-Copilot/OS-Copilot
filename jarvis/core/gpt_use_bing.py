import requests
import json
import os
from langchain.utilities import BingSearchAPIWrapper
from jarvis.action.get_os_version import get_os_version, check_os_version
from jarvis.core.llms import OpenAI

os.environ["BING_SUBSCRIPTION_KEY"] = "885e62a126554fb390af88ae31d2c8ff"
os.environ["BING_SEARCH_URL"] = "https://api.bing.microsoft.com/v7.0/search"
# search = BingSearchAPIWrapper()
 
# res = search.results("https://zhuanlan.zhihu.com/p/623421034 summary",10)
class ActionExecuter():
    """
    SkillCreator is used to generate new skills and store them in the action_lib.
    """
    def __init__(self, config_path=None) -> None:
        super().__init__()
        self.llm = OpenAI(config_path)
        self.tool = BingSearchAPIWrapper()
        self.system_version = get_os_version()
        try:
            check_os_version(self.system_version)
        except ValueError as e:
            print(e)
        # self.mac_systom_prompts = 

    def format_message(self, task, tool_input):
        observation = json.dumps(self.tool.results(tool_input,10),ensure_ascii=False,indent=4)
        self.prompt = '''
            You are a helpful assistant that can answer the user's questions with the help of tools.
            the feedbacks of the tools is as follows:
            {observation}
            You need to find the useful information in these feedbacks, cause some of then may not be helpful to answer the question.
            Once you find the useful information you need, please think it step by step to get the final answer with the help of the information.
            You should only respond with the final answer to the user.The final answer must be detail and reasonable.
            User's question:

        '''.format(observation = observation)
        # self.prompt = ""
        print(self.prompt)
        self.message = [
            {"role": "system", "content": self.prompt},
            {"role": "user", "content": task},
        ]
        return self.llm.chat(self.message)

res = ActionExecuter("../../examples/config.json").format_message("assistant api收费标准是什么?","open ai assistant api收费标准")        
print(res)
 
 
# """
#     Made by @wzm : 测试GPT使用web检索工具
# """
# headers = {
#             'Ocp-Apim-Subscription-Key': "885e62a126554fb390af88ae31d2c8ff"
# }
# url = "https://api.bing.microsoft.com/v7.0/search"

# querystring = {"q": "2x=5,x=?",
#                "mkt":"en-us",
#                "safeSearch": "Off"
#                }



# response = requests.get(url, headers=headers, params=querystring)
# data_list = response.json()
# # for each in data_list:
# #     print(each)
# # print(len(data_list["webPages"]["value"]))
with open("test.json", "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=4)