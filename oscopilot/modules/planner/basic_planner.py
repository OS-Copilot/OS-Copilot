from oscopilot.tool_repository.manager.action_node import ActionNode
from collections import defaultdict, deque
from oscopilot.modules.base_module import BaseModule
from oscopilot.tool_repository.manager.tool_manager import get_open_api_description_pair
from oscopilot.utils.utils import send_chat_prompts
import json
import sys
import logging


class BasicPlanner(BaseModule):
    """
    A planning module responsible for decomposing complex tasks into manageable subtasks, replanning tasks based on new insights or failures, and managing the execution order of tasks. 

    The `BasicPlanner` uses a combination of tool descriptions, environmental state, and language learning models to dynamically create and adjust plans for task execution. It maintains a tool list to manage task dependencies and execution order, ensuring that tasks are executed in a sequence that respects their interdependencies.
    """
    def __init__(self, prompt):
        super().__init__()
        self.subtask_num = 0
        self.prompt = prompt
        self.global_messages = []
        self.sub_task_list = []

    def reset_plan(self):
        """
        Resets global messages and subtask list to their initial states.
        """
        self.subtask_num = 0
        self.global_messages = []
        self.sub_task_list = []

    def decompose_task(self, task):
        """
        Decomposes a complex task into manageable subtasks.

        This method takes a high-level task and utilizes the environments's current state
        to format and send a decomposition request to the language learning model. It then 
        parses the response to construct and update the tool list with the decomposed subtasks.

        Args:
            task (str): The complex task to be decomposed.

        """
        sys_prompt = self.prompt['_SYSTEM_TASK_DECOMPOSE_PROMPT']
        user_prompt = self.prompt['_USER_TASK_DECOMPOSE_PROMPT'].format(
            system_version=self.system_version,
            task=task,
            working_dir=self.environment.working_dir
        )
        response = send_chat_prompts(sys_prompt, user_prompt, self.llm)
        print(response)
        task_list = self.extract_list_from_string(response)
        self.sub_task_list = task_list
        self.subtask_num = len(task_list)


    def replan_task(self, reasoning, current_task, relevant_tool_description_pair):
        """
        Replans the current task by integrating new tools into the original tool graph.

        Given the reasoning for replanning and the current task, this method generates a new
        tool plan incorporating any relevant tools. It formats a replanning request, sends
        it to the language learning model, and integrates the response (new tools) into the
        existing tool graph. The graph is then updated to reflect the new dependencies and
        re-sorted topologically.

        Args:
            reasoning (str): The reasoning or justification for replanning the task.
            current_task (str): The identifier of the current task being replanned.
            relevant_tool_description_pair (dict): A dictionary mapping relevant tool names to
                                                    their descriptions for replanning.

        Side Effects:
            Modifies the tool graph to include new tools and updates the execution order
            of tools within the graph.
        """
        # current_task information
        current_tool = self.tool_node[current_task]
        current_task_description = current_tool.description
        relevant_tool_description_pair = json.dumps(relevant_tool_description_pair)
        files_and_folders = self.environment.list_working_dir()
        sys_prompt = self.prompt['_SYSTEM_TASK_REPLAN_PROMPT']
        user_prompt = self.prompt['_USER_TASK_REPLAN_PROMPT'].format(
            current_task = current_task,
            current_task_description = current_task_description,
            system_version=self.system_version,
            reasoning = reasoning,
            tool_list = relevant_tool_description_pair,
            working_dir = self.environment.working_dir,
            files_and_folders = files_and_folders
        )
        response = send_chat_prompts(sys_prompt, user_prompt, self.llm)
        new_tool = self.extract_json_from_string(response)
        # add new tool to tool graph
        self.add_new_tool(new_tool, current_task)
        # update topological sort
        self.topological_sort()

    def update_tool(self, tool, return_val='', relevant_code=None, status=False, node_type='Code'):
        """
        Updates the specified tool's node information within the tool graph.

        This method allows updating an tool's return value, relevant code, execution status,
        and node_type. It is particularly useful for modifying tools' details after their execution
        or during the replanning phase.

        Args:
            tool (str): The tool identifier whose details are to be updated.
            return_val (str, optional): The return value of the tool. Default is an empty string.
            relevant_code (str, optional): Any relevant code associated with the tool. Default is None.
            status (bool, optional): The execution status of the tool. Default is False.
            node_type (str, optional): The node_type of the tool (e.g., 'Code'). Default is 'Code'.

        Side Effects:
            Updates the information of the specified tool node within the tool graph.
        """
        if return_val:
            if node_type=='Code':
                return_val = self.extract_information(return_val, "<return>", "</return>")
                print("************************<return>**************************")
                logging.info(return_val)
                print(return_val)
                print("************************</return>*************************")  
            if return_val != 'None':
                self.tool_node[tool]._return_val = return_val
        if relevant_code:
            self.tool_node[tool]._relevant_code = relevant_code
        self.tool_node[tool]._status = status

    def get_tool_list(self, relevant_tool=None):
        """
        Retrieves a list of all tools or a subset of relevant tools, including their names and descriptions.

        This method fetches tool descriptions from the tool library. If a specific set of relevant tools
        is provided, it filters the list to include only those tools. The resulting list (or the full list if
        no relevant tools are specified) is then returned in JSON format.

        Args:
            relevant_tool (list, optional): A list of tool names to filter the returned tools by.
                                            If None, all tools are included. Defaults to None.

        Returns:
            A JSON string representing a dictionary of tool names to their descriptions. 
            The dictionary includes either all tools from the library or only those specified as relevant.
        """
        tool_dict = self.tool_manager.descriptions
        if not relevant_tool:
            return json.dumps(tool_dict)
        relevant_tool_dict = {tool : description for tool ,description in tool_dict.items() if tool in relevant_tool}
        relevant_tool_list = json.dumps(relevant_tool_dict)
        return relevant_tool_list
    
    def create_tool_graph(self, decompose_json):
        """
        Constructs an tool graph based on dependencies specified in the given JSON.

        This method takes a JSON object containing task information and dependencies,
        and constructs an tool graph. Each task is added as a node in the graph, with
        directed edges representing task dependencies. The method updates the class's
        internal structures to reflect this graph, including tool nodes and their
        relationships, as well as the overall number of tools.

        Args:
            decompose_json (dict): A JSON object where each key is an tool name, and the value
                                is a dictionary containing the tool's name, description,
                                type, and dependencies.

        Side Effects:
            Modifies the internal state by updating `tool_num`, `tool_node`, and `tool_graph`
            to reflect the newly created tool graph.
        """
        for _, task_info in decompose_json.items():
            self.tool_num += 1
            task_name = task_info['name']
            task_description = task_info['description']
            task_type = task_info['type']
            task_dependencies = task_info['dependencies']
            self.tool_node[task_name] = ActionNode(task_name, task_description, task_type)
            self.tool_graph[task_name] = task_dependencies
            for pre_tool in self.tool_graph[task_name]:
                self.tool_node[pre_tool].next_action[task_name] = task_description
    
    def add_new_tool(self, new_task_json, current_task):
        """
        Incorporates a new tool into the existing tool graph based on its dependencies.

        This method processes a JSON object representing a new task, including its name,
        description, type, and dependencies, and adds it to the tool graph. It also updates
        the tool nodes to reflect this new addition. Finally, it appends the last new task
        to the list of dependencies for the specified current task.

        Args:
            new_task_json (dict): A JSON object containing the new task's details.
            current_task (str): The name of the current task to which the new task's dependencies will be added.

        Side Effects:
            Updates the tool graph and nodes to include the new tool and its dependencies.
            Modifies the dependencies of the current task to include the new tool.
        """
        for _, task_info in new_task_json.items():
            self.tool_num += 1
            task_name = task_info['name']
            task_description = task_info['description']
            task_type = task_info['type']
            task_dependencies = task_info['dependencies']
            self.tool_node[task_name] = ActionNode(task_name, task_description, task_type)
            self.tool_graph[task_name] = task_dependencies
            for pre_tool in self.tool_graph[task_name]:
                self.tool_node[pre_tool].next_action[task_name] = task_description           
        last_new_task = list(new_task_json.keys())[-1]
        self.tool_graph[current_task].append(last_new_task)
        
    def get_pre_tasks_info(self, current_task):
        """
        Retrieves information about the prerequisite tasks for a given current task.

        This method collects and formats details about all tasks that are prerequisites
        for the specified current task. It extracts descriptions and return values for
        each prerequisite task and compiles this information into a JSON string.

        Args:
            current_task (str): The name of the task for which prerequisite information is requested.

        Returns:
            A JSON string representing a dictionary, where each key is a prerequisite task's
            name, and the value is a dictionary with the task's description and return value.
        """
        pre_tasks_info = {}
        for task in self.tool_graph[current_task]:
            task_info = {
                "description" : self.tool_node[task].description,
                "return_val" : self.tool_node[task].return_val
            }
            pre_tasks_info[task] = task_info
        pre_tasks_info = json.dumps(pre_tasks_info)
        return pre_tasks_info


