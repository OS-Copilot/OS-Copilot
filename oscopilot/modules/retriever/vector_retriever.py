from oscopilot.modules.base_module import BaseModule
from oscopilot.utils.utils import send_chat_prompts
import json


class FridayRetriever(BaseModule):
    """
    A modules within the system responsible for retrieving and managing available tools from the tool library.

    The RetrievalModule extends the BaseModule class, focusing on the retrieval of tools
    based on specific prompts or queries. It interacts with a language learning model (LLM)
    and utilizes the execution environments and tool library to fulfill its responsibilities.
    """

    def __init__(self, prompt, tool_manager):
        super().__init__()
        self.prompt = prompt
        self.tool_manager = tool_manager

    def delete_tool(self, tool):
        """
        Deletes the specified tool from the tool library.

        This method calls the tool library's delete method to remove an tool by its name. It
        encompasses deleting the tool's code, description, parameters, and any other associated
        information.

        Args:
            tool (str): The name of the tool to be deleted.
        """
        self.tool_manager.delete_tool(tool)

    def retrieve_tool_name(self, task, k=10):        
        """
        Retrieves a list of tool names relevant to the specified task.

        This method interacts with the tool library to retrieve names of tools that are most
        relevant to a given task. The number of tool names returned is limited by the parameter k.

        Args:
            task (str): The task for which relevant tool names are to be retrieved.
            k (int, optional): The maximum number of tool names to retrieve. Defaults to 10.

        Returns:
            list[str]: A list of the top k tool names relevant to the specified task.
        """
        retrieve_tool_name = self.tool_manager.retrieve_tool_name(task, k)
        return retrieve_tool_name

    def tool_code_filter(self, tool_code_pair, task):
        """
        Filters and retrieves the code for an tool relevant to the specified task.

        This method formats a message for filtering tool codes based on a given task, sends
        the message to the tool library for processing, and retrieves the filtered tool's
        code. If an tool name is successfully identified, its corresponding code is fetched
        from the tool library.

        Args:
            tool_code_pair (dict): A dictionary mapping tool names to their codes.
            task (str): The task based on which the tool code needs to be filtered.

        Returns:
            The code of the tool relevant to the specified task, or an empty string
            if no relevant tool is found.
    """
        tool_code_pair = json.dumps(tool_code_pair)
        sys_prompt = self.prompt['_SYSTEM_ACTION_CODE_FILTER_PROMPT']
        user_prompt = self.prompt['_USER_ACTION_CODE_FILTER_PROMPT'].format(
            task_description=task,
            tool_code_pair=tool_code_pair
        )
        response = send_chat_prompts(sys_prompt, user_prompt, self.llm)
        tool_name = self.extract_information(response, '<action>', '</action>')[0]
        code = ''
        if tool_name:
            code = self.tool_manager.get_tool_code(tool_name)
        return code

    def retrieve_tool_description(self, tool_name):
        """
        Retrieves the description for a specified tool from the tool library.

        This method queries the tool library for the description of an tool identified
        by its name. It is designed to fetch detailed descriptions that explain what the
        tool does.

        Args:
            tool_name (str): The name of the tool whose description is to be retrieved.

        Returns:
            str: The description of the specified tool.
        """
        retrieve_tool_description = self.tool_manager.retrieve_tool_description(tool_name)
        return retrieve_tool_description  

    def retrieve_tool_code(self, tool_name):
        """
        Retrieves the code for a specified tool from the tool library.

        This method accesses the tool library to get the executable code associated with
        an tool identified by its name. This code defines how the tool is performed.

        Args:
            tool_name (str): The name of the tool whose code is to be retrieved.

        Returns:
            str: The code of the specified tool.
        """
        retrieve_tool_code = self.tool_manager.retrieve_tool_code(tool_name)
        return retrieve_tool_code 
    
    def retrieve_tool_code_pair(self, retrieve_tool_name):
        """
        Retrieves a mapping of tool names to their respective codes for a list of tools.

        This method processes a list of tool names, retrieving the code for each and
        compiling a dictionary that maps each tool name to its code. This is useful for
        tasks that require both the identification and the execution details of tools.

        Args:
            retrieve_tool_name (list[str]): A list of tool names for which codes are to be retrieved.

        Returns:
            dict: A dictionary mapping each tool name to its code.
        """
        retrieve_tool_code = self.retrieve_tool_code(retrieve_tool_name)
        tool_code_pair = {}
        for name, description in zip(retrieve_tool_name, retrieve_tool_code):
            tool_code_pair[name] = description
        return tool_code_pair        
        
    def retrieve_tool_description_pair(self, retrieve_tool_name):
        """
        Retrieves a mapping of tool names to their descriptions for a list of tools.

        By processing a list of tool names, this method fetches their descriptions and
        forms a dictionary that associates each tool name with its description. This
        facilitates understanding the purpose and functionality of multiple tools at once.

        Args:
            retrieve_tool_name (list[str]): A list of tool names for which descriptions are to be retrieved.

        Returns:
            dict: A dictionary mapping each tool name to its description.
        """
        retrieve_tool_description = self.retrieve_tool_description(retrieve_tool_name)
        tool_description_pair = {}
        for name, description in zip(retrieve_tool_name, retrieve_tool_description):
            tool_description_pair[name] = description
        return tool_description_pair


