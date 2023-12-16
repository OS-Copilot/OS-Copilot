from jarvis.agent.base_agent import BaseAgent
from jarvis.core.action_node import ActionNode
from collections import defaultdict, deque
from jarvis.environment.py_env import PythonEnv
from jarvis.core.llms import OpenAI
from jarvis.core.action_manager import ActionManager
from jarvis.action.get_os_version import get_os_version, check_os_version
from jarvis.core.llms import OpenAI
from jarvis.agent.prompt import prompt
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

    def __init__(self, config_path=None, action_lib_dir=None, max_iter=3):
        super().__init__()
        self.llm = OpenAI(config_path)
        self.action_lib = ActionManager(config_path, action_lib_dir)
        self.environment = PythonEnv()
        self.prompt = prompt
        self.system_version = get_os_version()
        self.planner = PlanningModule(self.llm, self.environment, self.action_lib, self.prompt['planning_prompt'], self.system_version)
        self.retriever = RetrievalModule(self.llm, self.environment, self.action_lib, self.prompt['retrieve_prompt'])
        self.executor = ExecutionModule(self.llm, self.environment, self.action_lib, self.prompt['execute_prompt'], self.system_version, max_iter)
        try:
            check_os_version(self.system_version)
        except ValueError as e:
            print(e)        

    def planning(self, task):
        # 综合处理任务的方法
        subtasks = self.planner.decompose_task(task)
        for subtask in subtasks:
            action = self.retriever.search_action(subtask)
            if action:
                result = self.executor.execute_action(action)
                # 进一步处理结果


class PlanningModule(BaseAgent):
    """ 规划模块，负责将复杂任务拆解为子任务 """

    def __init__(self, llm, environment, action_lib, prompt, system_version):
        # 模块初始化，包括设置执行环境，初始化prompt等
        super().__init__()
        # 模型，环境，数据库
        self.llm = llm
        self.environment = environment
        self.action_lib = action_lib
        self.system_version = system_version
        self.prompt = prompt
        # 动作节点，动作图信息和动作拓扑排序
        self.action_node = {}
        self.action_graph = defaultdict(list)
        self.action_list = []

    def decompose_task(self, task):
        # 实现任务拆解逻辑
        action_list = self.get_action_list
        files_and_folders = self.environment.list_working_dir()
        response = self.decompose_task_format_message(task, action_list, self.environment.working_dir, files_and_folders)
        decompose_json = self.extract_json_from_string(response)
        # 构建动作图和动作拓扑排序
        self.create_action_graph(decompose_json)
        self.topological_sort()
        # for _, node in self.action_node.items():
        #     print(node)

    def replan_task(self, reasoning, ):
        # 重新计划新的任务
        pass

    def add_task(self, new_action):
        # 将新的动作加入到动作图中
        self.create_action_graph(new_action)
        # 更新拓扑排序
        self.topological_sort()



    def update_action(self, action, code=None, return_val=None, status=False):
        # 更新动作节点信息
        if code:
            self.action_node[action].code = code
        if return_val:
            self.action_node[action].return_val = return_val
        self.action_node[action].status = status

    # Send decompse task prompt to LLM and get task list 
    def decompose_task_format_message(self, task, action_list, working_dir, files_and_folders):
        sys_prompt = self.prompt['_LINUX_SYSTEM_TASK_DECOMPOSE_PROMPT']
        user_prompt = self.prompt['_LINUX_USER_TASK_DECOMPOSE_PROMPT'].format(
            system_version=self.system_version,
            task=task,
            action_list = action_list,
            working_dir = working_dir,
            files_and_folders = files_and_folders
        )
        self.message = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt},
        ]
        return self.llm.chat(self.message)

    # Get action list, including action names and descriptions
    def get_action_list(self):
        action_dict = self.action_lib.descriptions
        action_list = json.dumps(action_dict)
        return action_list
    
    # Creates a action graph from a list of dependencies.
    def create_action_graph(self, json):
        # generate execte graph
        for task_name, task_info in json.items():
            self.action_node[task_name] = ActionNode(task_name, task_info['description'])
            self.action_graph[task_name] = task_info['dependencies']
    
    # generate graph topological sort
    def topological_sort(self):
        graph = defaultdict(list)
        for node, dependencies in self.action_graph.items():
            # If the current node has not been executed, put it in the dependency graph.
            if not self.action_node[node].status:
                graph.setdefault(node, [])
                for dependent in dependencies:
                    # If the dependencies of the current node have not been executed, put them in the dependency graph.
                    if not self.action_node[dependent].status:
                        graph[dependent].append(node)

        in_degree = {node: 0 for node in graph}      
        # Count in-degree for each node
        for node in graph:
            for dependent in graph[node]:
                in_degree[dependent] += 1

        # Initialize queue with nodes having in-degree 0
        queue = deque([node for node in in_degree if in_degree[node] == 0])

        # List to store the order of execution

        while queue:
            # Get one node with in-degree 0
            current = queue.popleft()
            self.action_list.append(current)

            # Decrease in-degree for all nodes dependent on current
            for dependent in graph[current]:
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)

        # Check if topological sort is possible (i.e., no cycle)
        if len(self.action_list) == len(graph):
            print("topological sort is possible")
        else:
            return "Cycle detected in the graph, topological sort not possible."




class RetrievalModule(BaseAgent):
    """ 检索模块，负责在动作库中检索可用动作 """

    def __init__(self, llm, environment, action_lib, prompt):
        # 模块初始化，包括设置执行环境，初始化prompt等
        super().__init__()
        # 模型，环境，数据库
        self.llm = llm
        self.environment = environment
        self.action_lib = action_lib
        self.prompt = prompt

    def search_action(self, subtask):
        # 实现检索动作逻辑
        pass


class ExecutionModule(BaseAgent):
    """ 执行模块，负责执行动作并更新动作库 """

    def __init__(self, llm, environment, action_lib, prompt, system_version, max_iter):
        # 模块初始化，包括设置执行环境，初始化prompt等
        super().__init__()
        # 模型，环境，数据库
        self.llm = llm
        self.environment = environment
        self.action_lib = action_lib
        self.system_version = system_version
        self.prompt = prompt
        self.max_iter = max_iter
    
    def generate_action(self, task_name, task_description):
        # 生成动作代码逻辑，生成可以完成动作的代码，返回生成的代码
        create_msg = self.skill_create_format_message(task_name, task_description, self.environment.working_dir)
        code = self.extract_python_code(create_msg)
        return code

    def execute_action(self, code, task_description):
        # 实现动作执行逻辑，实例化动作类并执行，返回执行完毕的状态
        invoke_msg = self.invoke_generate_format_message(code, task_description, self.environment.working_dir)
        invoke = self.extract_information(invoke_msg, begin_str='<invoke>', end_str='</invoke>')[0]
        code = code + '\n' + invoke
        print("************************<code>**************************")
        print(code)
        print("************************</code>*************************")  
        state = self.environment.step(code)
        print("************************<state>**************************")
        print(state)
        print("************************</state>*************************") 
        return state

    def judge_action(self, code, task_description, state):
        # 实现动作判断逻辑，判断动作是否完成当前任务，返回判断的JSON结果
        judge_json = self.task_judge_format_message(code, task_description, state.result, state.pwd, state.ls)
        reasoning = judge_json['reasoning']
        judge = judge_json['judge']
        score = judge_json['score']
        return reasoning, judge, score

    def amend_action(self, current_code, task_description, state, critique):
        # 实现动作修复逻辑，对于未完成任务或者有错误的代码进行修复，返回修复后的代码
        amend_msg = self.skill_amend_format_message(current_code, task_description, state.error, state.result, state.pwd, state.ls, critique)
        new_code = self.extract_python_code(amend_msg)
        return new_code

    def analysis_action(self, code, task_description, state):
        # 实现对代码错误的分析，如果是需要新的操作的环境错误，转到planning模块，否则交给amend_action，返回JSON
        analysis_json = self.error_analysis_format_message(code, task_description, state.error, state.pwd, state.ls)
        reasoning = analysis_json['reasoning']
        type = analysis_json['type']
        return reasoning, type
        
    def store_action(self, action, code):
        # 实现动作存储逻辑，对新的动作进行存储
        #  获取描述信息
        args_description = self.extract_args_description(code)
        action_description = self.extract_action_description(code)
        # 保存动作名称、代码，描述到JSON中
        action_info = self.save_action_info_to_json(action, code, action_description)
        # 保存代码，描述到数据库和JSON文件中
        self.action_lib.add_new_action(action_info)
        # 参数描述保存路径
        args_description_file_path = self.action_lib.action_lib_dir + '/args_description/' + action + '.txt'      
        # 保存参数
        self.save_str_to_path(args_description, args_description_file_path)

    # Send skill create message to LLM
    def skill_create_format_message(self, task_name, task_description, working_dir):
        sys_prompt = self.prompt['_LINUX_SYSTEM_SKILL_CREATE_PROMPT']
        user_prompt = self.prompt['_LINUX_USER_SKILL_CREATE_PROMPT'].format(
            system_version=self.system_version,
            task_description=task_description,
            working_dir=working_dir,
            task_name=task_name
        )
        self.message = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt},
        ]
        return self.llm.chat(self.message)

    # Send invoke generate message to LLM
    def invoke_generate_format_message(self, class_code, task_description, working_dir):
        class_name, args_description = self.extract_class_name_and_args_description(class_code)
        sys_prompt = self.prompt['_LINUX_SYSTEM_INVOKE_GENERATE_PROMPT']
        user_prompt = self.prompt['_LINUX_USER_INVOKE_GENERATE_PROMPT'].format(
            class_name = class_name,
            task_description = task_description,
            args_description = args_description,
            working_dir = working_dir
        )
        self.message = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt},
        ]
        return self.llm.chat(self.message)        
    
    # Send skill amend message to LLM
    def skill_amend_format_message(self, original_code, task, error, code_output, working_dir, files_and_folders, critique):
        sys_prompt = self.prompt['_LINUX_SYSTEM_SKILL_AMEND_PROMPT']
        user_prompt = self.prompt['_LINUX_USER_SKILL_AMEND_PROMPT'].format(
            original_code = original_code,
            task = task,
            error = error,
            code_output = code_output,
            working_dir = working_dir,
            files_and_folders = files_and_folders,
            critique = critique
        )
        self.message = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt},
        ]
        return self.llm.chat(self.message)    
    
    # Send task judge prompt to LLM and get JSON response
    def task_judge_format_message(self, current_code, task, code_output, working_dir, files_and_folders):
        sys_prompt = self.prompt['_LINUX_SYSTEM_TASK_JUDGE_PROMPT']
        user_prompt = self.prompt['_LINUX_USER_TASK_JUDGE_PROMPT'].format(
            current_code=current_code,
            task=task,
            code_output=code_output,
            working_dir=working_dir,
            files_and_folders= files_and_folders
        )
        self.message = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt},
        ]
        response =self.llm.chat(self.message)
        judge_json = self.extract_json_from_string(response)  
        print("************************<judge_json>**************************")
        print(judge_json)
        print("************************</judge_json>*************************")           
        return judge_json    

    # Send error analysis prompt to LLM and get JSON response
    def error_analysis_format_message(self, current_code, task, code_error, working_dir, files_and_folders):
        sys_prompt = self.prompt['_LINUX_SYSTEM_ERROR_ANALYSIS_PROMPT']
        user_prompt = self.prompt['_LINUX_USER_ERROR_ANALYSIS_PROMPT'].format(
            current_code=current_code,
            task=task,
            code_error=code_error,
            working_dir=working_dir,
            files_and_folders= files_and_folders
        )
        self.message = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt},
        ]
        response =self.llm.chat(self.message)
        analysis_json = self.extract_json_from_string(response)      
        print("************************<analysis_json>**************************")
        print(analysis_json)
        print("************************</analysis_json>*************************")           
        return analysis_json  

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
    
    # save str content to the specified path 
    def save_str_to_path(self, content, path):
        with open(path, 'w', encoding='utf-8') as f:
            lines = content.strip().splitlines()
            content = '\n'.join(lines)
            f.write(content)
                
    # save action info to json 
    def save_action_info_to_json(self, action, code, description):
        info = {
            "task_name" : action,
            "code": code,
            "description": description
        }
        return info


if __name__ == '__main__':
    agent = JarvisAgent(config_path='../../examples/config.json', action_lib_dir="../../jarvis/action_lib")
    json = agent.executor.error_analysis_format_message('''
    import pandas as pd
    import numpy as np

    # 创建一个包含随机数的DataFrame
    df = pd.DataFrame(np.random.randn(10, 4), columns=['A', 'B', 'C', 'D'])

    # 显示前几行数据
    print("DataFrame:")
    print(df)

    # 计算基本统计数据
    print("\nBasic Statistics:")
    print(df.describe())

    # 筛选出A列值大于0的行
    filtered_df = df[df['A'] > 0]
    print("\nRows where column A is greater than 0:")
    pint(filtered_df)


    ''',"Use pandas to operate on random arrays", '''
    Traceback (most recent call last):
    File "/home/heroding/桌面/Jarvis/working_dir/test.py", line 18, in <module>
        pint(filtered_df)
        ^^^^
    NameError: name 'pint' is not defined. Did you mean: 'print'?
    ''', "/home/heroding/桌面/Jarvis/tasks/travel/run_task", "cache  general.py  __pycache__  run.py  serve.py  simulator.py")
