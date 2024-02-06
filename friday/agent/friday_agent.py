from friday.agent.base_agent import BaseAgent
from friday.core.action_node import ActionNode
from collections import defaultdict, deque
from friday.environment.py_env import PythonEnv
from friday.core.llms import OpenAI
from friday.core.action_manager import ActionManager
from friday.action.get_os_version import get_os_version, check_os_version
from friday.agent.prompt import prompt
from friday.core.utils import get_open_api_description_pair, get_open_api_doc_path
import re
import json
import logging

class FridayAgent(BaseAgent):
    """ AI agent class, including planning, retrieval and execution modules """

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

    def run(self, task):
        """
        Run FridayAgent to execute task.
        """
        # relevant action 
        retrieve_action_name = self.retriever.retrieve_action_name(task)
        retrieve_action_description_pair = self.retriever.retrieve_action_description_pair(retrieve_action_name)

        # decompose task
        self.planner.decompose_task(task, retrieve_action_description_pair)

        # iter each subtask
        while self.planner.execute_list:
            action = self.planner.execute_list[0]
            action_node = self.planner.action_node[action]
            description = action_node.description
            logging.info("The current subtask is: {subtask}".format(subtask=description))
            code = ''
            # The return value of the current task
            result = ''
            next_action = action_node.next_action
            relevant_code = {}
            type = action_node.type
            pre_tasks_info = self.planner.get_pre_tasks_info(action)
            if type == 'Code':
                # retrieve existing action
                retrieve_name = self.retriever.retrieve_action_name(description, 3)
                relevant_code = self.retriever.retrieve_action_code_pair(retrieve_name)
            # task execute step
            if type == 'QA':
                # result = self.executor.question_and_answer_action(pre_tasks_info, task, task)
                if self.planner.action_num == 1:
                    result = self.executor.question_and_answer_action(pre_tasks_info, task, task)
                else:
                    result = self.executor.question_and_answer_action(pre_tasks_info, task, description)
                print(result)
                logging.info(result)
            else:
                invoke = ''
                if type == 'API':
                    api_path = self.executor.extract_API_Path(description)
                    code = self.executor.api_action(description, api_path, pre_tasks_info)
                else:
                    code, invoke = self.executor.generate_action(action, description, pre_tasks_info, relevant_code)
                # Execute python tool class code
                state = self.executor.execute_action(code, invoke, type)   
                result = state.result 
                logging.info(state)
            # Check whether the code runs correctly, if not, amend the code
            if type == 'Code':
                need_mend = False
                trial_times = 0
                critique = ''
                score = 0
                # If no error is reported, check whether the task is completed
                if state.error == None:
                    critique, judge, score = self.executor.judge_action(code, description, state, next_action)
                    if not judge:
                        print("critique: {}".format(critique))
                        need_mend = True
                else:
                    #  Determine whether it is caused by an error outside the code
                    reasoning, error_type = self.executor.analysis_action(code, description, state)
                    if error_type == 'replan':
                        relevant_action_name = self.retriever.retrieve_action_name(reasoning)
                        relevant_action_description_pair = self.retriever.retrieve_action_description_pair(relevant_action_name)
                        self.planner.replan_task(reasoning, action, relevant_action_description_pair)
                        continue
                    need_mend = True   
                # The code failed to complete its task, fix the code
                while (trial_times < self.executor.max_iter and need_mend == True):
                    trial_times += 1
                    print("current amend times: {}".format(trial_times))
                    new_code, invoke = self.executor.amend_action(code, description, state, critique, pre_tasks_info)
                    critique = ''
                    code = new_code
                    # Run the current code and check for errors
                    state = self.executor.execute_action(code, invoke, type)
                    result = state.result
                    logging.info(state) 
                    # print(state)
                    # Recheck
                    if state.error == None:
                        critique, judge, score = self.executor.judge_action(code, description, state, next_action)
                        # The task execution is completed and the loop exits
                        if judge:
                            need_mend = False
                            break
                        # print("critique: {}".format(critique))
                    else: # The code still needs to be corrected
                        need_mend = True

                # If the task still cannot be completed, an error message will be reported.
                if need_mend == True:
                    print("I can't Do this Task!!")
                    break
                else: # The task is completed, if code is save the code, args_description, action_description in lib
                    if score >= 8:
                        self.executor.store_action(action, code)
            print("Current task execution completed!!!")  
            self.planner.update_action(action, result, relevant_code, True, type)
            self.planner.execute_list.remove(action)


class PlanningModule(BaseAgent):
    """ The planning module is responsible for breaking down complex tasks into subtasks, re-planning, etc. """

    def __init__(self, llm, environment, action_lib, prompt, system_version):
        """
        Module initialization, including setting the execution environment, initializing prompts, etc.
        """
        super().__init__()
        # Model, environment, database
        self.llm = llm
        self.environment = environment
        self.action_lib = action_lib
        self.system_version = system_version
        self.prompt = prompt
        # Action nodes, action graph information and action topology sorting
        self.action_num = 0
        self.action_node = {}
        self.action_graph = defaultdict(list)
        self.execute_list = []

    def decompose_task(self, task, action_description_pair):
        """
        Implement task disassembly logic.
        """
        files_and_folders = self.environment.list_working_dir()
        action_description_pair = json.dumps(action_description_pair)
        response = self.task_decompose_format_message(task, action_description_pair, files_and_folders)
        logging.info(f"The overall response is: {response}")
        decompose_json = self.extract_json_from_string(response)
        # Building action graph and topological ordering of actions
        self.create_action_graph(decompose_json)
        self.topological_sort()

    def replan_task(self, reasoning, current_task, relevant_action_description_pair):
        """
        replan new task to origin action graph .
        """
        # current_task information
        current_action = self.action_node[current_task]
        current_task_description = current_action.description
        relevant_action_description_pair = json.dumps(relevant_action_description_pair)
        files_and_folders = self.environment.list_working_dir()
        response = self.task_replan_format_message(reasoning, current_task, current_task_description, relevant_action_description_pair, files_and_folders)
        new_action = self.extract_json_from_string(response)
        # add new action to action graph
        self.add_new_action(new_action, current_task)
        # update topological sort
        self.topological_sort()

    def update_action(self, action, return_val='', relevant_code=None, status=False, type='Code'):
        """
        Update action node info.
        """
        if return_val:
            if type=='Code':
                return_val = self.extract_information(return_val, "<return>", "</return>")
                print("************************<return>**************************")
                logging.info(return_val)
                print(return_val)
                print("************************</return>*************************")  
            if return_val != 'None':
                self.action_node[action]._return_val = return_val
        if relevant_code:
            self.action_node[action]._relevant_code = relevant_code
        self.action_node[action]._status = status

    def task_decompose_format_message(self, task, action_list, files_and_folders):
        """
        Send decompse task prompt to LLM and get task list.
        """
        api_list = get_open_api_description_pair()
        sys_prompt = self.prompt['_SYSTEM_TASK_DECOMPOSE_PROMPT']
        user_prompt = self.prompt['_USER_TASK_DECOMPOSE_PROMPT'].format(
            system_version=self.system_version,
            task=task,
            action_list = action_list,
            api_list = api_list,
            working_dir = self.environment.working_dir,
            files_and_folders = files_and_folders
        )
        self.message = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt},
        ]
        return self.llm.chat(self.message)
      
    def task_replan_format_message(self, reasoning, current_task, current_task_description, action_list, files_and_folders):
        """
        Send replan task prompt to LLM and get task list.
        """
        sys_prompt = self.prompt['_SYSTEM_TASK_REPLAN_PROMPT']
        user_prompt = self.prompt['_USER_TASK_REPLAN_PROMPT'].format(
            current_task = current_task,
            current_task_description = current_task_description,
            system_version=self.system_version,
            reasoning = reasoning,
            action_list = action_list,
            working_dir = self.environment.working_dir,
            files_and_folders = files_and_folders
        )
        self.message = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt},
        ]
        return self.llm.chat(self.message)

    def get_action_list(self, relevant_action=None):
        """
        Get action list, including action names and descriptions.
        """
        action_dict = self.action_lib.descriptions
        if not relevant_action:
            return json.dumps(action_dict)
        relevant_action_dict = {action : description for action ,description in action_dict.items() if action in relevant_action}
        relevant_action_list = json.dumps(relevant_action_dict)
        return relevant_action_list
    
    def create_action_graph(self, decompose_json):
        """
        Creates a action graph from a list of dependencies.
        """
        # generate execte graph
        for _, task_info in decompose_json.items():
            self.action_num += 1
            task_name = task_info['name']
            task_description = task_info['description']
            task_type = task_info['type']
            task_dependencies = task_info['dependencies']
            self.action_node[task_name] = ActionNode(task_name, task_description, task_type)
            self.action_graph[task_name] = task_dependencies
            for pre_action in self.action_graph[task_name]:
                self.action_node[pre_action].next_action[task_name] = task_description

    
    def add_new_action(self, new_task_json, current_task):
        """
        Creates a action graph from a list of dependencies.
        """
        # update execte graph
        for _, task_info in new_task_json.items():
            self.action_num += 1
            task_name = task_info['name']
            task_description = task_info['description']
            task_type = task_info['type']
            task_dependencies = task_info['dependencies']
            self.action_node[task_name] = ActionNode(task_name, task_description, task_type)
            self.action_graph[task_name] = task_dependencies
            for pre_action in self.action_graph[task_name]:
                self.action_node[pre_action].next_action[task_name] = task_description           
        last_new_task = list(new_task_json.keys())[-1]
        self.action_graph[current_task].append(last_new_task)

    def topological_sort(self):
        """
        generate graph topological sort.
        """
        # init execute list
        self.execute_list = []
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
            self.execute_list.append(current)

            # Decrease in-degree for all nodes dependent on current
            for dependent in graph[current]:
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)

        # Check if topological sort is possible (i.e., no cycle)
        if len(self.execute_list) == len(graph):
            print("topological sort is possible")
        else:
            return "Cycle detected in the graph, topological sort not possible."
        
    def get_pre_tasks_info(self, current_task):
        """
        Get string information of the prerequisite task for the current task.
        """
        pre_tasks_info = {}
        for task in self.action_graph[current_task]:
            task_info = {
                "description" : self.action_node[task].description,
                "return_val" : self.action_node[task].return_val
            }
            pre_tasks_info[task] = task_info
        pre_tasks_info = json.dumps(pre_tasks_info)
        return pre_tasks_info



class RetrievalModule(BaseAgent):
    """ Retrieval module, responsible for retrieving available actions in the action library. """

    def __init__(self, llm, environment, action_lib, prompt):
        """
        Module initialization, including setting the execution environment, initializing prompts, etc.
        """
        super().__init__()
        # Model, environment, database
        self.llm = llm
        self.environment = environment
        self.action_lib = action_lib
        self.prompt = prompt

    def delete_action(self, action):
        """
        Delete relevant action content, including code, description, parameter information, etc.
        """
        self.action_lib.delete_action(action)

    def retrieve_action_name(self, task, k=10):        
        """
        Implement retrieval action name logic
        """
        retrieve_action_name = self.action_lib.retrieve_action_name(task, k)
        return retrieve_action_name

    def action_code_filter(self, action_code_pair, task):
        """
        Implement filtering of search codes.
        """
        action_code_pair = json.dumps(action_code_pair)
        response = self.action_code_filter_format_message(action_code_pair, task)
        action_name = self.extract_information(response, '<action>', '</action>')[0]
        code = ''
        if action_name:
            code = self.action_lib.get_action_code(action_name)
        return code

    def retrieve_action_description(self, action_name):
        """
        Implement search action description logic.
        """
        retrieve_action_description = self.action_lib.retrieve_action_description(action_name)
        return retrieve_action_description  

    def retrieve_action_code(self, action_name):
        """
        Implement retrieval action code logic.
        """
        retrieve_action_code = self.action_lib.retrieve_action_code(action_name)
        return retrieve_action_code 
    
    def retrieve_action_code_pair(self, retrieve_action_name):
        """
        Retrieve task code pairs.
        """
        retrieve_action_code = self.retrieve_action_code(retrieve_action_name)
        action_code_pair = {}
        for name, description in zip(retrieve_action_name, retrieve_action_code):
            action_code_pair[name] = description
        return action_code_pair        
        
    def retrieve_action_description_pair(self, retrieve_action_name):
        """
        Retrieve task description pairs.
        """
        retrieve_action_description = self.retrieve_action_description(retrieve_action_name)
        action_description_pair = {}
        for name, description in zip(retrieve_action_name, retrieve_action_description):
            action_description_pair[name] = description
        return action_description_pair
    
    def action_code_filter_format_message(self, action_code_pair, task_description):
        """
        Send aciton code to llm to filter useless action codes.
        """
        sys_prompt = self.prompt['_SYSTEM_ACTION_CODE_FILTER_PROMPT']
        user_prompt = self.prompt['_USER_ACTION_CODE_FILTER_PROMPT'].format(
            task_description=task_description,
            action_code_pair=action_code_pair
        )
        self.message = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt},
        ]
        return self.llm.chat(self.message)    


class ExecutionModule(BaseAgent):
    """ Execution module, responsible for executing actions and updating the action library """

    def __init__(self, llm, environment, action_lib, prompt, system_version, max_iter):
        '''
        Module initialization, including setting the execution environment, initializing prompts, etc.
        '''
        super().__init__()
        self.llm = llm
        self.environment = environment
        self.action_lib = action_lib
        self.system_version = system_version
        self.prompt = prompt
        self.max_iter = max_iter
        self.open_api_doc_path = get_open_api_doc_path()
        self.open_api_doc = {}
        with open(self.open_api_doc_path) as f:
            self.open_api_doc = json.load(f) 
    
    def generate_action(self, task_name, task_description, pre_tasks_info, relevant_code):
        '''
        Generate action code logic, generate code that can complete the action and its calls.
        '''
        relevant_code = json.dumps(relevant_code)
        create_msg = self.skill_create_and_invoke_format_message(task_name, task_description, pre_tasks_info, relevant_code)
        code = self.extract_python_code(create_msg)
        invoke = self.extract_information(create_msg, begin_str='<invoke>', end_str='</invoke>')[0]
        return code, invoke

    # def generate_action(self, task_name, task_description):
    #     '''
    #     Generate action code logic, generate code that can complete the action and its calls.
    #     '''
    #     create_msg = self.skill_create_format_message(task_name, task_description)
    #     code = self.extract_python_code(create_msg)
    #     return code

    def execute_action(self, code, invoke, type):
        '''
        Implement action execution logic.
        instantiate the action class and execute it, and return the execution completed status.
        '''
        # print result info
        if type == 'Code':
            info = "\n" + '''print("<return>")''' + "\n" + "print(result)" +  "\n" + '''print("</return>")'''
            code = code + '\nresult=' + invoke + info
        print("************************<code>**************************")
        print(code)
        print("************************</code>*************************")  
        state = self.environment.step(code)
        print("************************<state>**************************")
        print(state)
        # print("error: " + state.error + "\nresult: " + state.result + "\npwd: " + state.pwd + "\nls: " + state.ls)
        print("************************</state>*************************") 
        return state

    # def execute_action(self, code, task_description, pre_tasks_info):
    #     '''
    #     Implement action execution logic.
    #     instantiate the action class and execute it, and return the execution completed status.
    #     '''
    #     invoke_msg = self.invoke_generate_format_message(code, task_description, pre_tasks_info)
    #     invoke = self.extract_information(invoke_msg, begin_str='<invoke>', end_str='</invoke>')[0]
    #     # print result info
    #     info = "\n" + '''print("<return>")''' + "\n" + "print(result)" +  "\n" + '''print("</return>")'''
    #     code = code + '\nresult=' + invoke + info
    #     print("************************<code>**************************")
    #     print(code)
    #     print("************************</code>*************************")  
    #     state = self.environment.step(code)
    #     print("************************<state>**************************")
    #     print(state)
    #     print("************************</state>*************************") 
    #     return state

    def judge_action(self, code, task_description, state, next_action):
        '''
        Implement action judgment logic.
        judge whether the action completes the current task, and return the JSON result of the judgment.
        '''
        judge_json = self.task_judge_format_message(code, task_description, state.result, state.pwd, state.ls, next_action)
        reasoning = judge_json['reasoning']
        judge = judge_json['judge']
        score = judge_json['score']
        return reasoning, judge, score

    def amend_action(self, current_code, task_description, state, critique, pre_tasks_info):
        '''
        Implement action repair logic.
        repair unfinished tasks or erroneous code, and return the repaired code and call.
        '''
        amend_msg = self.skill_amend_and_invoke_format_message(current_code, task_description, state.error, state.result, state.pwd, state.ls, critique, pre_tasks_info)
        new_code = self.extract_python_code(amend_msg)
        invoke = self.extract_information(amend_msg, begin_str='<invoke>', end_str='</invoke>')[0]
        return new_code, invoke

    # def amend_action(self, current_code, task_description, state, critique):
    #     '''
    #     Implement action repair logic.
    #     repair unfinished tasks or erroneous code, and return the repaired code and call.
    #     '''
    #     amend_msg = self.skill_amend_format_message(current_code, task_description, state.error, state.result, state.pwd, state.ls, critique)
    #     new_code = self.extract_python_code(amend_msg)
    #     return new_code

    def analysis_action(self, code, task_description, state):
        '''
        Implement the analysis of code errors. 
        If it is an environmental error that requires new operations, go to the planning module. 
        Otherwise, hand it to amend_action and return JSON.
        '''
        analysis_json = self.error_analysis_format_message(code, task_description, state.error, state.pwd, state.ls)
        reasoning = analysis_json['reasoning']
        type = analysis_json['type']
        return reasoning, type
        
    def store_action(self, action, code):
        """
        Store action code and info.
        
        """
        # If action not in db.
        if not self.action_lib.exist_action(action):
            # Implement action storage logic and store new actions
            args_description = self.extract_args_description(code)
            action_description = self.extract_action_description(code)
            # Save action name, code, and description to JSON
            action_info = self.save_action_info_to_json(action, code, action_description)
            # Save code and descriptions to databases and JSON files
            self.action_lib.add_new_action(action_info)
            # Parameter description save path
            args_description_file_path = self.action_lib.action_lib_dir + '/args_description/' + action + '.txt'      
            # save args_description
            self.save_str_to_path(args_description, args_description_file_path)
        else:
            print("action already exists!")


    def api_action(self, description, api_path, context="No context provided."):
        """
        Call api tool to execute task.
        """
        response = self.generate_call_api_format_message(description, api_path, context)
        code = self.extract_python_code(response)
        return code 
    
    def question_and_answer_action(self, context, question, current_question=None):
        """
        Answer questions based on the information found.
        """
        response = self.question_and_answer_format_message(context, question, current_question)
        return response

    def skill_create_and_invoke_format_message(self, task_name, task_description, pre_tasks_info, relevant_code):
        """
        Send skill generate and invoke message to LLM.
        """
        sys_prompt = self.prompt['_SYSTEM_SKILL_CREATE_AND_INVOKE_PROMPT']
        user_prompt = self.prompt['_USER_SKILL_CREATE_AND_INVOKE_PROMPT'].format(
            system_version=self.system_version,
            task_description=task_description,
            working_dir= self.environment.working_dir,
            task_name=task_name,
            pre_tasks_info=pre_tasks_info,
            relevant_code=relevant_code
        )
        self.message = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt},
        ]
        return self.llm.chat(self.message)

    def skill_create_format_message(self, task_name, task_description):
        """
        Send skill create message to LLM.
        """
        sys_prompt = self.prompt['_SYSTEM_SKILL_CREATE_PROMPT']
        user_prompt = self.prompt['_USER_SKILL_CREATE_PROMPT'].format(
            system_version=self.system_version,
            task_description=task_description,
            working_dir= self.environment.working_dir,
            task_name=task_name
        )
        self.message = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt},
        ]
        return self.llm.chat(self.message)

    def invoke_generate_format_message(self, class_code, task_description, pre_tasks_info):
        """
        Send invoke generate message to LLM.
        """
        class_name, args_description = self.extract_class_name_and_args_description(class_code)
        sys_prompt = self.prompt['_SYSTEM_INVOKE_GENERATE_PROMPT']
        user_prompt = self.prompt['_USER_INVOKE_GENERATE_PROMPT'].format(
            class_name = class_name,
            task_description = task_description,
            args_description = args_description,
            pre_tasks_info = pre_tasks_info,
            working_dir = self.environment.working_dir
        )
        self.message = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt},
        ]
        return self.llm.chat(self.message)        
    
    def question_and_answer_format_message(self, context, question, current_question):
        """
        Send QA message to LLM.
        """
        sys_prompt = self.prompt['_SYSTEM_QA_PROMPT']
        user_prompt = self.prompt['_USER_QA_PROMPT'].format(
            context = context,
            question = question,
            current_question = current_question
        )
        self.message = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt},
        ]
        return self.llm.chat(self.message)      
 
    def skill_amend_and_invoke_format_message(self, original_code, task, error, code_output, current_working_dir, files_and_folders, critique, pre_tasks_info):
        """
        Send skill amend message to LLM.
        """
        sys_prompt = self.prompt['_SYSTEM_SKILL_AMEND_AND_INVOKE_PROMPT']
        user_prompt = self.prompt['_USER_SKILL_AMEND_AND_INVOKE_PROMPT'].format(
            original_code = original_code,
            task = task,
            error = error,
            code_output = code_output,
            current_working_dir = current_working_dir,
            working_dir= self.environment.working_dir,
            files_and_folders = files_and_folders,
            critique = critique,
            pre_tasks_info = pre_tasks_info
        )
        self.message = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt},
        ]
        return self.llm.chat(self.message)   

    def skill_amend_format_message(self, original_code, task, error, code_output, current_working_dir, files_and_folders, critique):
        """
        Send skill amend message to LLM.
        """
        sys_prompt = self.prompt['_SYSTEM_SKILL_AMEND_PROMPT']
        user_prompt = self.prompt['_USER_SKILL_AMEND_PROMPT'].format(
            original_code = original_code,
            task = task,
            error = error,
            code_output = code_output,
            current_working_dir = current_working_dir,
            working_dir= self.environment.working_dir,
            files_and_folders = files_and_folders,
            critique = critique
        )
        self.message = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt},
        ]
        return self.llm.chat(self.message)    
    
    def task_judge_format_message(self, current_code, task, code_output, current_working_dir, files_and_folders, next_action):
        """
        Send task judge prompt to LLM and get JSON response.
        """
        next_action = json.dumps(next_action)
        sys_prompt = self.prompt['_SYSTEM_TASK_JUDGE_PROMPT']
        user_prompt = self.prompt['_USER_TASK_JUDGE_PROMPT'].format(
            current_code=current_code,
            task=task,
            code_output=code_output,
            current_working_dir=current_working_dir,
            working_dir=self.environment.working_dir,
            files_and_folders=files_and_folders,
            next_action=next_action
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

    def error_analysis_format_message(self, current_code, task, code_error, current_working_dir, files_and_folders):
        """
        Send error analysis prompt to LLM and get JSON response.
        """
        sys_prompt = self.prompt['_SYSTEM_ERROR_ANALYSIS_PROMPT']
        user_prompt = self.prompt['_USER_ERROR_ANALYSIS_PROMPT'].format(
            current_code=current_code,
            task=task,
            code_error=code_error,
            current_working_dir=current_working_dir,
            working_dir= self.environment.working_dir,
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

    def extract_python_code(self, response):
        """
        Extract python code from response.
        """
        python_code = ""
        if '```python' in response:
            python_code = response.split('```python')[1].split('```')[0]
        elif '```' in python_code:
            python_code = response.split('```')[1].split('```')[0]
        return python_code    

    def extract_class_name_and_args_description(self, class_code):
        """
        Extract class_name and args description from python code.
        """
        class_name_pattern = r"class (\w+)"
        class_name_match = re.search(class_name_pattern, class_code)
        class_name = class_name_match.group(1) if class_name_match else None

        # Extracting the __call__ method's docstring
        call_method_docstring_pattern = r"def __call__\([^)]*\):\s+\"\"\"(.*?)\"\"\""
        call_method_docstring_match = re.search(call_method_docstring_pattern, class_code, re.DOTALL)
        args_description = call_method_docstring_match.group(1).strip() if call_method_docstring_match else None

        return class_name, args_description
    
    def extract_args_description(self, class_code):
        """
        Extract args description from python code.
        """
        # Extracting the __call__ method's docstring
        call_method_docstring_pattern = r"def __call__\([^)]*\):\s+\"\"\"(.*?)\"\"\""
        call_method_docstring_match = re.search(call_method_docstring_pattern, class_code, re.DOTALL)
        args_description = call_method_docstring_match.group(1).strip() if call_method_docstring_match else None
        return args_description

    def extract_action_description(self, class_code):
        """
        Extract action description from python code.
        """
        # Extracting the __init__ method's description
        init_pattern = r"def __init__\s*\(self[^)]*\):\s*(?:.|\n)*?self\._description\s*=\s*\"([^\"]+)\""
        action_match = re.search(init_pattern, class_code, re.DOTALL)
        action_description = action_match.group(1).strip() if action_match else None
        return action_description
    
    def save_str_to_path(self, content, path):
        """
        save str content to the specified path. 
        """
        with open(path, 'w', encoding='utf-8') as f:
            lines = content.strip().splitlines()
            content = '\n'.join(lines)
            f.write(content)
                 
    def save_action_info_to_json(self, action, code, description):
        """
        save action info to json. 
        """
        info = {
            "task_name" : action,
            "code": code,
            "description": description
        }
        return info
    
    def generate_call_api_format_message(self, tool_sub_task, tool_api_path, context="No context provided."):
        self.sys_prompt = self.prompt['_SYSTEM_TOOL_USAGE_PROMPT'].format(
            openapi_doc = json.dumps(self.generate_openapi_doc(tool_api_path)),
            tool_sub_task = tool_sub_task,
            context = context
        )
        self.user_prompt = self.prompt['_USER_TOOL_USAGE_PROMPT']
        self.message = [
            {"role": "system", "content": self.sys_prompt},
            {"role": "user", "content": self.user_prompt},
        ]
        return self.llm.chat(self.message)
    
    def generate_openapi_doc(self, tool_api_path):
        """
        Format openapi document.
        """
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
        # json格式
        if (("requestBody" in findptr) and 
        ("content" in findptr["requestBody"]) and 
        ("application/json" in findptr["requestBody"]["content"]) and 
        ("schema" in findptr["requestBody"]["content"]["application/json"]) and 
        ("$ref" in findptr["requestBody"]["content"]["application/json"]["schema"])):
            api_params_schema_ref = findptr["requestBody"]["content"]["application/json"]["schema"]["$ref"]
        elif (("requestBody" in findptr) and 
        ("content" in findptr["requestBody"]) and 
        ("multipart/form-data" in findptr["requestBody"]["content"]) and 
        ("schema" in findptr["requestBody"]["content"]["multipart/form-data"]) and 
        ("allOf" in findptr["requestBody"]["content"]["multipart/form-data"]["schema"]) and 
        ("$ref" in findptr["requestBody"]["content"]["multipart/form-data"]["schema"]["allOf"][0])):
            api_params_schema_ref = findptr["requestBody"]["content"]["multipart/form-data"]["schema"]["allOf"][0]["$ref"]
        if api_params_schema_ref != None and api_params_schema_ref != "":
            curr_api_doc["components"]["schemas"][api_params_schema_ref.split('/')[-1]] = self.open_api_doc["components"]["schemas"][api_params_schema_ref.split('/')[-1]]
        return curr_api_doc

    def extract_API_Path(self, text):
        """
        Extracts UNIX-style and Windows-style paths from the given string,
        handling paths that may be enclosed in quotes.

        :param s: The string from which to extract paths.
        :return: A list of extracted paths.
        """
        # Regular expression for UNIX-style and Windows-style paths
        unix_path_pattern = r"/[^/\s]+(?:/[^/\s]*)*"
        windows_path_pattern = r"[a-zA-Z]:\\(?:[^\\\/\s]+\\)*[^\\\/\s]+"

        # Combine both patterns
        pattern = f"({unix_path_pattern})|({windows_path_pattern})"

        # Find all matches
        matches = re.findall(pattern, text)

        # Extract paths from the tuples returned by findall
        paths = [match[0] or match[1] for match in matches]

        # Remove enclosing quotes (single or double) from the paths
        stripped_paths = [path.strip("'\"") for path in paths]
        return stripped_paths[0]



if __name__ == '__main__':
    agent = FridayAgent(config_path='../../examples/config.json', action_lib_dir="friday/action_lib")
    print(agent.executor.extract_API_Path('''Use the "/tools/arxiv' API to search for the autogen paper and retrieve its summary.'''))
