import requests
import json
import os
from jarvis.action.get_os_version import get_os_version, check_os_version
from jarvis.core.llms import OpenAI
from jarvis.core.tools_dict import tools_dict

# search = BingSearchAPIWrapper()
 
# res = search.results("https://zhuanlan.zhihu.com/p/623421034 summary",10)
class ActionExecuter():
    """
    SkillCreator is used to generate new skills and store them in the action_lib.
    """
    def __init__(self, config_path=None) -> None:
        super().__init__()
        self.llm = OpenAI(config_path)
        self.tool_dict = tools_dict
        self.system_version = get_os_version()
        try:
            check_os_version(self.system_version)
        except ValueError as e:
            print(e)
        # self.mac_systom_prompts = 

    def respond_with_tools(self, task, tool_name,tool_input):
        tool = self.tool_dict[tool_name]
        observation = json.dumps(tool(tool_input),ensure_ascii=False,indent=4)
        self.prompt = '''
            You are a helpful assistant that can answer the user's questions with the help of tools.
            the feedbacks of the tool named {tool_name} is as follows:
            {observation}
            You need to find the useful information in these feedbacks, cause some of then may not be helpful to answer the question.
            Once you find the useful information you need, please think it step by step to get the final answer with the help of the information.
            At most time,you should only respond with the final answer to the user.The final answer must be detail and reasonable.
            If you are using the search engine tool which returns top k relavant retrieved results, and you find its feedbacks are too simplified
            to help you to get the final correct answer, you can choice the most relavant one and use its link as the input of the web browser tool 
            to get the detailed content of the web page,you need to tell the user if you want to use the web browser tool to load the web page in 
            a following format:
            I need to browser the page: <tool>web_browser("the link you select")</tool>
            User's question:

        '''.format(tool_name=tool_name,observation = observation)
        # self.prompt = ""
        print(self.prompt)
        self.message = [
            {"role": "system", "content": self.prompt},
            {"role": "user", "content": task},
        ]
        return self.llm.chat(self.message)
    def extract_information(self, message, begin_str='[BEGIN]', end_str='[END]'):
        result = []
        _begin = message.find(begin_str)
        _end = message.find(end_str)
        while not (_begin == -1 or _end == -1):
            result.append(message[_begin + len(begin_str):_end].strip())
            message = message[_end + len(end_str):]
            _begin = message.find(begin_str)
            _end = message.find(end_str)
        return result  
q = '''
How many studio albums were published by Mercedes Sosa between 2000 and 2009 (included)?
'''
# q = '''
# 介绍一下华东师范大学数据学院的院长
# '''
tool_agent = ActionExecuter("../../examples/config.json")
res = tool_agent.respond_with_tools(q,"bing_search",q)    
print(res)
next_tool = tool_agent.extract_information(res, begin_str='<tool>', end_str='</tool>')
if len(next_tool) > 0:
    if(next_tool[0].startswith("web_browser")):
        link = tool_agent.extract_information(next_tool[0], begin_str='("', end_str='")')[0]
        print("======================browsering...======================")
        

        final_res = tool_agent.respond_with_tools(q,"web_browser",link)
        print(final_res)

 
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
