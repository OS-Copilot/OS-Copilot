import json
import re
import os
import ast
import time
import openai
import copy
import requests
from collections import defaultdict

from jarvis.core.prompt import TRAVEL_SYSTEM_PROMPT, TRAVEL_USER_FIRST, TRAVEL_USER_OVER_PROMPT, TRAVEL_USER_PROMPT, TRAVEL_EXAMPLE_MESSAGES_1
# from agents.base_agent import BaseAgent
# from utils.prompt import generate_prompt
# from utils.api_service import chat_gpt


class BaseAgent:
    def __init__(self, record_path=None, model_name='gpt-3.5-turbo', proxy='http://127.0.0.1:10809'):
        self.system_prompt = None
        self.messages = []
        self.subtasks = []
        self.model_name = model_name
        self.proxy = proxy
        self.record_path = record_path

    def chat_gpt(self, messages, model_name="gpt-3.5-turbo-16k-0613", sleep_time=2, temperature=0,proxy=None):
        # if proxy is not None:
        #     os.environ["http_proxy"] = proxy
        #     os.environ["https_proxy"] = proxy

        openai.api_key = os.getenv("OPENAI_API_KEY")
        org=os.getenv("OPENAI_ORGANIZATION")
        print(f'message[-1]={messages[-1]}')
        if org is not None:
            openai.organization=org
        try:
            response = openai.chat.completions.create(
                model=model_name,
                messages=messages,
                temperature=temperature,
                timeout=60
            )
        except openai.RateLimitError as e:
            print(e)
            time.sleep(60)
            response = openai.ChatCompletion.create(
                model=model_name,
                messages=messages,
                temperature=temperature,
                timeout=60
            )
        except openai.InternalServerError as e2:
            print(e2)
            time.sleep(60)
            response = openai.ChatCompletion.create(
                model=model_name,
                messages=messages,
                temperature=temperature,
                timeout=60
            )
        print(f'response={response}')
        time.sleep(sleep_time)
        # if proxy is not None:
        #     os.environ.pop("http_proxy", None)
        #     os.environ.pop("https_proxy", None)
        
        return {'role': response.choices[0].message.role, 'content': response.choices[0].message.content}


    def gpt_4(self, messages, model_name="gpt-4-1106-preview", sleep_time=2, temperature=0, session=None, proxy=None):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        url = "https://api.openai-hk.com/v1/chat/completions"

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(openai.api_key)
        }

        data = {
            "max_tokens": 1200,
            "model": model_name,
            "temperature": temperature,
            "top_p": 1,
            "presence_penalty": 1,
            "messages": messages
        }

        response = session.post(url, headers=headers, data=json.dumps(data).encode('utf-8') )
        result = response.content.decode("utf-8")

        print(f'response={result}')
        result = ast.literal_eval(result)
        time.sleep(sleep_time)
        return {'role': result['choices'][0]['message']['role'], 'content': result['choices'][0]['message']['content']}



    def parse_functions(self, text):
        def extract_functions(text: str, begin="<action>", end='</action>') -> list:
            # 提取所有被 <action> 和 </action> 包围的内容
            actions = re.findall(f"{re.escape(begin)}(.*?){re.escape(end)}", text, re.DOTALL)

            result = []
            for action in actions:
                # 匹配函数名和参数
                match = re.match(r"(\w+)\((.*?)\)$", action.strip(), re.DOTALL)
                if match:
                    function_name, args = match.groups()
                    args = args.strip()
                    # 处理参数字符串，保证它们被引号包围
                    if args:
                        # 匹配由三重引号包围的多行字符串
                        multi_line_str_match = re.match(r"(['\"]{3})(.*?)\1", args, re.DOTALL)
                        if multi_line_str_match:
                            args = [multi_line_str_match.group(2)]
                        else:
                            # 分割参数，并去除两侧的空白和引号
                            args = [arg.strip().strip('"').strip("'") for arg in args.split(',')]
                    else:
                        args = []

                    result.append({
                        "function_name": function_name,
                        "args": args
                    })

            return result

        # def extract_functions(text: str, begin="<action>", end='</action>') -> list:
        #     action_patterns = re.findall(rf'{begin}(.*?){end}', text, re.DOTALL)
        #     result = []
        #
        #     for pattern in action_patterns:
        #         # 提取函数名称和参数
        #         match = re.match(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*\((.*)\)', pattern, re.DOTALL)
        #
        #         if match:
        #             function_name = match.group(1)
        #             args_raw = match.group(2).strip()
        #
        #             # 检查是否存在参数
        #             if args_raw == "" or re.match(r'^[\'"].*[\'"]$', args_raw, re.DOTALL):
        #                 # 手动解析参数
        #                 delimiter_stack = []
        #                 current_arg = ""
        #                 args = []
        #                 escape = False
        #                 for char in args_raw:
        #                     if char == "\\" and not escape:
        #                         escape = True
        #                         current_arg += char
        #                         continue
        #
        #                     if escape:
        #                         escape = False
        #                         current_arg += char
        #                         continue
        #
        #                     if char in ["'", '"'] and (not delimiter_stack or delimiter_stack[-1] == char):
        #                         if delimiter_stack and delimiter_stack[-1] == char:
        #                             delimiter_stack.pop()
        #                         else:
        #                             delimiter_stack.append(char)
        #                         current_arg += char
        #                     elif char == "," and not delimiter_stack:
        #                         args.append(current_arg.strip(" '\""))
        #                         current_arg = ""
        #                     else:
        #                         current_arg += char
        #
        #                 if current_arg:
        #                     args.append(current_arg.strip(" '\""))
        #
        #                 result.append({
        #                     "function_name": function_name,
        #                     "args": args
        #                 })
        #     return result

        functions = extract_functions(text=text)
        return functions


    def get_action_space(self):
        # 使用正则表达式来匹配所有的action
        action_pattern = re.compile(r'<action>(.*?)\((.*?)\)</action>')
        actions = action_pattern.findall(self.system_prompt)

        # 用于存储action和其参数
        action_dict = defaultdict(list)

        for action_name, params in actions:
            params_list = params.split(',') if params else []
            params_list = [param.strip() for param in params_list]
            # 记录参数数量最多的action
            if len(params_list) > len(action_dict[action_name]):
                action_dict[action_name] = params_list

        # 构建最终的action list
        result = []
        for action_name, params in action_dict.items():
            if params:
                action_str = f'<action>{action_name}({", ".join(params)})</action>'
            else:
                action_str = f'<action>{action_name}()</action>'
            result.append(action_str)

        return result


    def get_subtasks(self, text):
        pattern = r'<subtask>(.*?)<\/subtask>'
        matches = re.findall(pattern, text, re.DOTALL)
        subtasks = []
        for match in matches:
            subtask_data = json.loads(match)
            subtasks.append(subtask_data)
        return subtasks


    def get_subtask_idx(self, subtask_name):
        for i, subtask in enumerate(self.subtasks):
            if subtask["subtask_name"] == subtask_name:
                return i
        return -1


    def add_subtask(self, subtasks):
        for subtask in subtasks:
            idx = self.get_subtask_idx(subtask['subtask_name'])
            if idx >= 0:
                self.subtasks[idx] = subtask
            else:
                self.subtasks.append(subtask)


    def add_user_prompt(self, observation):
        self.messages.append({'role': 'user', 'content': f'{observation}'})


    def add_user_error_prompt(self, observation):
        self.add_user_prompt(observation)


    def get_response(self, session):
        if 'gpt-4' in self.model_name:
            response = self.gpt_4(messages=self.messages, model_name=self.model_name, session=session, proxy=self.proxy)
        else:
            response = self.chat_gpt(messages=self.messages, model_name=self.model_name, proxy=self.proxy)
        self.messages.append(response)
        if self.record_path is not None:
            with open(self.record_path, 'w', encoding='utf-8') as f:
                json.dump(self.messages, f, indent=4, ensure_ascii=False)
        subtasks = self.get_subtasks(response['content'])
        self.add_subtask(subtasks)
        return response


class ReactAgent(BaseAgent):
    def __init__(self, task, record_path=None, model_name='gpt-3.5-turbo', proxy='http://127.0.0.1:10809',example_message=TRAVEL_EXAMPLE_MESSAGES_1):
        super().__init__(record_path=record_path, model_name=model_name, proxy=proxy)
        self.task = task
        self.subtasks = []
        self.completed_tasks = []
        self.system_prompt = self.generate_system_prompt()
        self.messages.append({'role': 'system',
                              'content': self.system_prompt})
        self.action_apace = self.get_action_space()
        self.messages.extend(example_message)
        self.messages.append({'role': 'user',
                              'content': self.generate_first_user_prompt(task=self.task)})

    
    def generate_prompt(self, template: str, replace_dict: dict):
        prompt = copy.deepcopy(template)
        for k, v in replace_dict.items():
            prompt = prompt.replace(k, str(v))
        return prompt


    def generate_system_prompt(self):
        system_prompt = TRAVEL_SYSTEM_PROMPT
        replace_dict = {
        }
        return self.generate_prompt(template=system_prompt, replace_dict=replace_dict)


    def generate_first_user_prompt(self, task):
        user_prompt = TRAVEL_USER_FIRST
        replace_dict = {
            '{{task}}': task
        }
        return self.generate_prompt(template=user_prompt, replace_dict=replace_dict)


    def add_user_prompt(self, observation):
        user_prompt = TRAVEL_USER_PROMPT
        replace_dict = {
            '{{observation}}': observation,
            '{{action_space}}': str(self.action_apace)
        }
        prompt = self.generate_prompt(template=user_prompt, replace_dict=replace_dict)
        self.messages.append({'role': 'user', 'content': prompt})


    def add_over_prompt(self):
        self.messages.append({'role': 'user', 'content': TRAVEL_USER_OVER_PROMPT})


if __name__ == '__main__':
    react_agent = ReactAgent()