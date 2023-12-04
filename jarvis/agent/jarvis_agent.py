from jarvis.agent.base_agent import BaseAgent
from jarvis.core.llms import OpenAI
from jarvis.core.utils import generate_prompt
from jarvis.action.get_os_version import get_os_version, check_os_version
from jarvis.core.llms import OpenAI
from jarvis.agent.prompt import prompt_dict
import re
import json


USER_PROMPT='''
Task: {task}

'''
PLANNING_SYSTEM_PROMPT = '''

'''
PLANNING_EXAMPLE_MESSAGES = [{'role': 'system', 'name': 'example_user',
                     'content': '''Task Requirements: Bob is in Shanghai and going to travel in several cities, please make a ticket purchase plan and travel sequence for him.The demands are as follows:
1. visit ['Beijing']. The order doesn't matter and he needs to return to Shanghai finally.
2. He is free to travel from 2023.7.1 to 2023.7.20. The budget for transportation is 1000.0 CNY.
3. Play at least 3 days in Beijing.
4. If you arrive in a city before 12:00 noon, that day can be counted as a day of play. If it's past 12 o'clock, it doesn't count as a day.
5. On the basis of completing the above conditions (especially the budget), spend as little time as possible.
'''},
                    {'role': 'system', 'name': 'example_assistant', 'content':
                        '''Based on the requirements, we can know that Bob need to go to Beijing from Shanghai, stay in Beijing for 3 days and then go to Shanghai from Beijing.
Given the task, the first step is to find available train tickets that fit Bob's schedule and budget. This is a subtask that requires the use of external resources, so I will assign it to another agent.
<subtask>
{
"subtask_name": "find_available_train_tickets",
"goal": "Find train tickets from Shanghai to Beijing and back to Shanghai that fit within the travel dates, budget, and allow for at least 3 full days of play in Beijing. If the arrival is before 12:00 noon, it counts as a day of play.",
"criticism": "Must ensure that the total cost of the round trip tickets does not exceed the budget of 1000.0 CNY and that the timings allow for at least 3 full days in Beijing. For each ticket, you must give me the ticket number, origin, destination, departure time, arrival time and the price.",
"milestones": ["Identify a suitable train from Shanghai to Beijing that arrives before 12:00 noon, ensuring a day of play.", "Identify a return train from Beijing to Shanghai after at least 3 days in Beijing.", "Ensure the total cost of both tickets is within the budget of 1000.0 CNY."]
}
</subtask>
<action>subagent_handle("find_available_train_tickets")</action>

Once I receive the information about the train tickets, I will proceed with planning the rest of Bob's travel schedule.
'''},

                    {'role': 'system', 'name': 'example_user',
                     'content': '''Action:
<action>subagent_handle("find_available_train_tickets")</action>
Result:
For Bob's travel from Beijing to Chengdu and back, the updated option is:
- Departure on train **G1371** from Beijing to Chengdu on **2023-07-02 08:57**, arriving at **2023-07-02 17:54**. This costs **747.0 CNY** and takes approximately 8 hours 57 minutes.
- Return on train **K1382** from Chengdu to Beijing on **2023-07-02 19:04**, arriving at **2023-07-03 11:52**. This costs **252.0 CNY** and takes about 16 hours 48 minutes.
The total round trip costs **999.0 CNY** and will take about 25 hours 45 minutes.
For future planning:
With this new itinerary, Bob will be able to spend a full 24 hours in Chengdu.
Bob can now proceed to research places of interest in Chengdu and plan his day accordingly. He can use the 'place' and 'in_city_transport' tables for this purpose.
Bob should also consider the transport options within Chengdu, ensuring he can visit his chosen destinations without spending too much time commuting.
'''},
                    {'role': 'system', 'name': 'example_assistant', 'content':
                        '''Next we can get the final plan. This task is simple so I can do it without other agents. We just need to use go_to_city() and stay_in() here. Based on the information provided, here is the final travel plan for Bob:
<plan>go_to_city("Beijing", "Chengdu", "2023-07-02 08:57", "2023-07-02 17:54", "G1371")</plan>
<plan>stay_in("Chengdu", "2023-07-02 17:54", "2023-07-03 17:54")</plan>
<plan>go_to_city("Chengdu", "Beijing", "2023-07-03 19:04", "2023-07-04 11:52", "K1382")</plan>
The task is completed. <action>over()</over>
'''}]






class JarvisAgent(BaseAgent):
    """ AI代理类，包含规划、检索和执行模块 """

    def __init__(self, config_path=None):
        super().__init__()
        self.llm = OpenAI(config_path)
        self.planner = PlanningModule(self.llm)
        self.retriever = RetrievalModule()
        self.executor = ExecutionModule()

    def planning(self, task):
        # 综合处理任务的方法
        subtasks = self.planner.decompose_task(task)
        for subtask in subtasks:
            action = self.retriever.search_action(subtask)
            if action:
                result = self.executor.execute_action(action)
                # 进一步处理结果


class PlanningModule:
    """ 规划模块，负责将复杂任务拆解为子任务 """

    def __init__(self, llm:OpenAI=None, system_replace_dict:dict=None):
        # 初始化代码，如设置初始参数
        if llm == None:
            raise NotImplementedError
        self.llm = llm
        self.messages = []
        self.system_prompt = generate_prompt(PLANNING_SYSTEM_PROMPT, replace_dict=system_replace_dict)
        self.messages.append({'role': 'system',
                              'content': self.system_prompt})
        self.messages.extend(PLANNING_EXAMPLE_MESSAGES)


    def decompose_task(self, task):
        # 实现任务拆解逻辑
        self.user_prompt = USER_PROMPT.format(
            task=task
        )
        self.messages.append({'role': 'user',
                              'content': self.user_prompt})
        response = self.llm.chat(self.messages)
        response_text = response['content']
        # TODO: 解析出子任务
        return response_text


class RetrievalModule:
    """ 检索模块，负责在动作库中检索可用动作 """

    def __init__(self):
        # 初始化代码，如动作库的加载
        pass

    def search_action(self, subtask):
        # 实现检索动作逻辑
        pass


class ExecutionModule:
    """ 执行模块，负责执行动作并更新动作库 """

    def __init__(self, config_path=None):
        # 模块初始化，包括设置执行环境，初始化prompt等
        super().__init__()
        self.llm = OpenAI(config_path)
        self.system_version = get_os_version()
        self.prompt = prompt_dict
        try:
            check_os_version(self.system_version)
        except ValueError as e:
            print(e)
    
    def generate_action(self, task_name, task_description, working_dir):
        # 生成动作代码逻辑，生成可以完成动作的代码，返回生成的代码
        create_msg = self.skill_create_format_message(task_name, task_description, working_dir)
        code = self.extract_python_code(create_msg)
        return code

    def execute_action(self, environment, code, task_description, working_dir):
        # 实现动作执行逻辑，实例化动作类并执行，返回执行完毕的状态
        invoke_msg = self.invoke_generate_format_message(code, task_description, working_dir)
        invoke = self.extract_information(invoke_msg, begin_str='<invoke>', end_str='</invoke>')[0]
        code = code + '\n' + invoke
        state = environment.step(code)
        return state

    def judge_action(self, code, task_description, state):
        # 实现动作判断逻辑，判断动作是否完成当前任务，返回判断的JSON结果
        judge_json = self.task_judge_format_message(code, task_description, state.result, state.pwd, state.ls)
        critique = judge_json['reasoning']
        score = judge_json['score']
        return critique, score

    def amend_action(self, current_code, task_description, state, critique):
        # 实现动作修复逻辑，对于未完成任务或者有错误的代码进行修复，返回修复后的代码
        amend_msg = self.skill_amend_format_message(current_code, task_description, state.error, state.result, state.pwd, state.ls, critique)
        new_code = self.extract_python_code(amend_msg)[0]
        return new_code

        
    def store_action(self, code):
        # 实现动作存储逻辑，对于没有问题的动作代码，对其代码、描述、参数信息、返回信息进行存储
        pass

    # Send skill create message to LLM
    def skill_create_format_message(self, task_name, task_description, working_dir):
        self.sys_prompt = self.prompt['_LINUX_SYSTEM_SKILL_CREATE_PROMPT']
        self.user_prompt = self.prompt['_LINUX_USER_SKILL_CREATE_PROMPT'].format(
            system_version=self.system_version,
            task_description=task_description,
            working_dir=working_dir,
            task_name=task_name
        )
        self.message = [
            {"role": "system", "content": self.sys_prompt},
            {"role": "user", "content": self.user_prompt},
        ]
        return self.llm.chat(self.message)

    # Send invoke generate message to LLM
    def invoke_generate_format_message(self, class_code, task_description,working_dir):
        class_name, args_description = self.extract_class_name_and_args_description(class_code)
        self.sys_prompt = self.prompt['_LINUX_SYSTEM_INVOKE_GENERATE_PROMPT']
        self.user_prompt = self.prompt['_LINUX_USER_INVOKE_GENERATE_PROMPT'].format(
           class_name = class_name,
           task_description = task_description,
           args_description = args_description,
           working_dir = working_dir
        )
        self.message = [
            {"role": "system", "content": self.sys_prompt},
            {"role": "user", "content": self.user_prompt},
        ]
        return self.llm.chat(self.message)        
    
    # Send skill amend message to LLM
    def skill_amend_format_message(self, original_code, task, error,code_output,working_dir,files_and_folders,critique):
        self.sys_prompt = self.prompt['_LINUX_SYSTEM_SKILL_AMEND_PROMPT']
        self.user_prompt = self.prompt['_LINUX_USER_SKILL_AMEND_PROMPT'].format(
           original_code = original_code,
           task = task,
           error = error,
           code_output = code_output,
            working_dir = working_dir,
            files_and_folders = files_and_folders,
            critique = critique
        )
        self.message = [
            {"role": "system", "content": self.sys_prompt},
            {"role": "user", "content": self.user_prompt},
        ]
        return self.llm.chat(self.message)    
    
    # Send task judge prompt to LLM and get JSON response
    def task_judge_format_message(self, current_code,task,code_output,working_dir,files_and_folders):
        self.sys_prompt = self.prompt['_LINUX_SYSTEM_TASK_JUDGE_PROMPT']
        self.user_prompt = self.prompt['_LINUX_TASK_JUDGE_PROMPT'].format(
           current_code=current_code,
           task=task,
           code_output=code_output,
           working_dir=working_dir,
           files_and_folders= files_and_folders
        )
        self.message = [
            {"role": "system", "content": self.sys_prompt},
            {"role": "user", "content": self.user_prompt},
        ]
        response =self.llm.chat(self.message)
        judge_json = '{' + '\n' + self.extract_information(response, '{', '}')[0] + '\n' + '}'    
        print("************************<judge_json>**************************")
        print(judge_json)
        print("************************</judge_json>*************************")           
        judge_json = json.loads(judge_json)
        return judge_json    

    # Extract python code from response
    def extract_python_code(self, response):
        python_code = ""
        if '```python' in response:
            python_code = response.split('```python')[1].split('```')[0]
        elif '```' in python_code:
            python_code = response.split('```')[1].split('```')[0]
        return python_code    

    # Extract class_name and args description from python code
    def extract_class_name_and_args_description(self, class_code):
        class_name_pattern = r"class (\w+)"
        class_name_match = re.search(class_name_pattern, class_code)
        class_name = class_name_match.group(1) if class_name_match else None

        # Extracting the __call__ method's docstring
        call_method_docstring_pattern = r"def __call__\([^)]*\):\s+\"\"\"(.*?)\"\"\""
        call_method_docstring_match = re.search(call_method_docstring_pattern, class_code, re.DOTALL)
        args_description = call_method_docstring_match.group(1).strip() if call_method_docstring_match else None

        return class_name, args_description
    
    # Extract args description from python code
    def extract_args_description(self, class_code):
        # Extracting the __call__ method's docstring
        call_method_docstring_pattern = r"def __call__\([^)]*\):\s+\"\"\"(.*?)\"\"\""
        call_method_docstring_match = re.search(call_method_docstring_pattern, class_code, re.DOTALL)
        args_description = call_method_docstring_match.group(1).strip() if call_method_docstring_match else None
        return args_description

    # Extract action description from python code
    def extract_action_description(self, class_code):
        # Extracting the __init__ method's description
        init_pattern = r"def __init__\s*\(self[^)]*\):\s*(?:.|\n)*?self\._description\s*=\s*\"([^\"]+)\""
        action_match = re.search(init_pattern, class_code, re.DOTALL)
        action_description = action_match.group(1).strip() if action_match else None
        return action_description
         
    # Extract information from text
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


# 示例使用
# agent = AIAgent()
# agent.process_task("示例任务")
