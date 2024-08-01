from oscopilot.tool_repository.manager.action_node import ActionNode
from collections import defaultdict, deque
from oscopilot.modules.base_module import BaseModule
from oscopilot.tool_repository.manager.tool_manager import get_open_api_description_pair
from oscopilot.utils.utils import send_chat_prompts, api_exception_mechanism
import json
import sys
import logging


class FridayPlanner(BaseModule):
    """
    A planning module responsible for decomposing complex tasks into manageable subtasks, replanning tasks based on new insights or failures, and managing the execution order of tasks. 

    The `FridayPlanner` uses a combination of tool descriptions, environmental state, and language learning models to dynamically create and adjust plans for task execution. It maintains a tool graph to manage task dependencies and execution order, ensuring that tasks are executed in a sequence that respects their interdependencies.
    """
    def __init__(self, prompt):
        super().__init__()
        self.tool_num = 0
        self.tool_node = {}
        self.prompt = prompt
        self.tool_graph = defaultdict(list)
        self.sub_task_list = []

    def reset_plan(self):
        """
        Resets the tool graph and subtask list to their initial states.
        """
        self.tool_num = 0
        self.tool_node = {}
        self.tool_graph = defaultdict(list)
        self.sub_task_list = []

    @api_exception_mechanism(max_retries=3)
    def decompose_task(self, task, tool_description_pair):
        """
        Decomposes a complex task into manageable subtasks and updates the tool graph.

        This method takes a high-level task and an tool-description pair, and utilizes
        the environments's current state to format and send a decomposition request to the
        language learning model. It then parses the response to construct and update the
        tool graph with the decomposed subtasks, followed by a topological sort to
        determine the execution order.

        Args:
            task (str): The complex task to be decomposed.
            tool_description_pair (dict): A dictionary mapping tool names to their descriptions.

        Side Effects:
            Updates the tool graph with the decomposed subtasks and reorders tools based on
            dependencies through topological sorting.
        """
        files_and_folders = self.environment.list_working_dir()
        tool_description_pair = json.dumps(tool_description_pair)
        api_list = get_open_api_description_pair()
        sys_prompt = self.prompt['_SYSTEM_TASK_DECOMPOSE_PROMPT']
        user_prompt = self.prompt['_USER_TASK_DECOMPOSE_PROMPT'].format(
            system_version=self.system_version,
            task=task,
            tool_list = tool_description_pair,
            api_list = api_list,
            working_dir = self.environment.working_dir,
            files_and_folders = files_and_folders
        )
        response = send_chat_prompts(sys_prompt, user_prompt, self.llm, prefix="Overall")
        decompose_json = self.extract_json_from_string(response)
        # Building tool graph and topological ordering of tools
        if decompose_json != 'No JSON data found in the string.':
            self.create_tool_graph(decompose_json)
            self.topological_sort()
        else:
            print(response)
            print('No JSON data found in the string.')
            sys.exit()

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
        for task_name, task_info in decompose_json.items():
            self.tool_num += 1
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
        for task_name, task_info in new_task_json.items():
            self.tool_num += 1
            task_description = task_info['description']
            task_type = task_info['type']
            task_dependencies = task_info['dependencies']
            self.tool_node[task_name] = ActionNode(task_name, task_description, task_type)
            self.tool_graph[task_name] = task_dependencies
            for pre_tool in self.tool_graph[task_name]:
                self.tool_node[pre_tool].next_action[task_name] = task_description           
        last_new_task = list(new_task_json.keys())[-1]
        self.tool_graph[current_task].append(last_new_task)

    def topological_sort(self):
        """
        Generates a topological sort of the tool graph to determine the execution order.

        This method applies a topological sorting algorithm to the current tool graph, 
        considering the status of each tool. It aims to identify an order in which tools
        can be executed based on their dependencies, ensuring that all prerequisites are met
        before an tool is executed. The sorting algorithm accounts for tools that have not
        yet been executed to avoid cycles and ensure a valid execution order.

        Side Effects:
            Populates `sub_task_list` with the sorted order of tools to be executed if a 
            topological sort is possible. Otherwise, it indicates a cycle detection.
        """
        self.sub_task_list = []
        graph = defaultdict(list)
        for node, dependencies in self.tool_graph.items():
            # If the current node has not been executed, put it in the dependency graph.
            if not self.tool_node[node].status:
                graph.setdefault(node, [])
                for dependent in dependencies:
                    # If the dependencies of the current node have not been executed, put them in the dependency graph.
                    if not self.tool_node[dependent].status:
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
            self.sub_task_list.append(current)

            # Decrease in-degree for all nodes dependent on current
            for dependent in graph[current]:
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)

        # Check if topological sort is possible (i.e., no cycle)
        if len(self.sub_task_list) == len(graph):
            print("topological sort is possible")
        else:
            return "Cycle detected in the graph, topological sort not possible."
        
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


