from jarvis.core.llms import OpenAI
from jarvis.environment.py_env import PythonEnv
import json
'''
让大模型根据目标工具的API文档做网络请求，获取到响应数据并返回
'''
TOOL_SYS_PROMPT='''
You are a useful AI assistant capable of accessing APIs to complete user-specified tasks, according to API documentation, 
by using the provided ToolRequestUtil tool. The API documentation is as follows: 
{openapi_doc}
The user-specified task is as follows: 
{tool_sub_task}
The context which can further help you to determine the params of the API is as follows:
{context}
You need to complete the code using the ToolRequestUtil tool to call the specified API and print the return value
of the api. 
ToolRequestUtil is a utility class, and the parameters of its 'request' method are described as follows:
def request(self, api_path, method, params=None, content_type=None):
    """
    :param api_path: the path of the API
    :param method: get/post
    :param params: the parameters of the API, can be None
    :param content_type: the content type of the API, e.g., application/json, can be None
    :return: the response from the API
    """
Please begin your code completion:

'''

TOOL_USER_PROMPT='''
from jarvis.core.tool_request_util import ToolRequestUtil
tool_request_util = ToolRequestUtil()
# TODO: your code here
'''

class ToolAgent():
    ''' ToolAgent is used to call the tool api and get the result feedback '''
    def __init__(self, config_path=None, open_api_doc_path = None) -> None:
        super().__init__()
        self.llm = OpenAI(config_path)
        self.open_api_doc = {}
        self.environment = PythonEnv()
        with open(open_api_doc_path) as f:
            self.open_api_doc = json.load(f) 
        # self.mac_systom_prompts = 

    def generate_call_api_code(self, tool_sub_task,tool_api_path,context="No context provided."):
        self.sys_prompt = TOOL_SYS_PROMPT.format(
            openapi_doc = json.dumps(self.generate_openapi_doc(tool_api_path)),
            tool_sub_task = tool_sub_task,
            context = context
        )
        self.user_prompt = TOOL_USER_PROMPT
        self.message = [
            {"role": "system", "content": self.sys_prompt},
            {"role": "user", "content": self.user_prompt},
        ]
        return self.llm.chat(self.message)
    def generate_openapi_doc(self, tool_api_path):
        # init current api's doc
        curr_api_doc = {}
        curr_api_doc["openapi"] = self.open_api_doc["openapi"]
        curr_api_doc["info"] = self.open_api_doc["info"]
        curr_api_doc["paths"] = {}
        curr_api_doc["components"] = {"schemas":{}}
        api_path_doc = {}
        #extract path and schema
        if tool_api_path not in self.open_api_doc["paths"]:
            curr_api_doc = {"error": "The api is not existed"}
            return curr_api_doc
        api_path_doc = self.open_api_doc["paths"][tool_api_path]
        curr_api_doc["paths"][tool_api_path] = api_path_doc
        find_ptr = {}
        if "get" in api_path_doc:
            findptr  = api_path_doc["get"]
        elif "post" in api_path_doc:
            findptr = api_path_doc["post"]
        api_params_schema_ref = ""
        if (("requestBody" in findptr) and 
        ("content" in findptr["requestBody"]) and 
        ("application/json" in findptr["requestBody"]["content"]) and 
        ("schema" in findptr["requestBody"]["content"]["application/json"]) and 
        ("$ref" in findptr["requestBody"]["content"]["application/json"]["schema"])):
            api_params_schema_ref = findptr["requestBody"]["content"]["application/json"]["schema"]["$ref"]
        if api_params_schema_ref != None and api_params_schema_ref != "":
            curr_api_doc["components"]["schemas"][api_params_schema_ref.split('/')[-1]] = self.open_api_doc["components"]["schemas"][api_params_schema_ref.split('/')[-1]]
            
        return curr_api_doc
    def extract_python_code(self, response):
        python_code = ""
        if '```python' in response:
            python_code = response.split('```python')[1].split('```')[0]
        elif '```' in python_code:
            python_code = response.split('```')[1].split('```')[0]
        return python_code
    def execute_code(self,code):
        state = self.environment.step(code)
        api_result = None;
        if(state.error != None and state.error != ""):
            api_result = state.error
        else:
            api_result = state.result
        return api_result

        
# agent = ToolAgent("../../examples/config.json","../core/openapi.json")
# code_text = agent.generate_call_api_code("use /tools/bing/searchv2 tool to search How many studio albums were published by Mercedes Sosa between 2000 and 2009 (included)? You can use the latest 2022 version of english wikipedia.","/tools/bing/searchv2")
# code = agent.extract_python_code(code_text)
# print(code)
# api_res = agent.execute_code(code)
# print(api_res)