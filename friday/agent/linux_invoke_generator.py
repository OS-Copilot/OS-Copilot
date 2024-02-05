from jarvis.action.get_os_version import get_os_version, check_os_version
import re
from jarvis.core.llms import OpenAI

_LINUX_SYSTEM_INVOKE_GENERATOR_PROMPT = '''
You are an AI trained to assist with Python programming tasks, with a focus on class and method usage.
Your goal is to generate a Python __call__ method invocation statement based on provided class names, task descriptions, and method parameter details.
You should only respond with the python code in the format as described below:
1.Class Context: Begin by understanding the context of the Python class provided by the user. This includes grasping the class name and its intended functionality.
2.Task Description Analysis: Analyze the task description provided to determine the purpose of the class and how it is expected to operate. This will help in identifying the correct method of the class to invoke.
3.Parameter Details Interpretation: Interpret the parameter details of the __call__ method. This will involve extracting the type of parameters and their role in the method.
4.Generating Invocation Statement: Construct the __call__ method invocation statement. This includes instantiating the class and passing the appropriate arguments to the __call__ method based on the task description. For example, if my class is called abc, and its __call__ method takes parameters 1 and 2, then my call statement could be abc()(1,2)
5.Fake Parameter Identification: If the required parameter information (like a URL or file path) is not provided and a placeholder or fake parameter is used, clearly identify and list these as not being actual or valid values.All the fake paramters you list should be separated by comma.If there are no fake parameters,you should give a None.
6.Output Format: The final output should include two parts:The first one is the invocation statement,which will be enclosed in <invoke></invoke> tags.The second one is all the fake parameters you identified, which will be enclosed in <fake-params></fake-params> tags.
And the response you write should also follow the following criteria:
Criteria:
1.The __call__ method invocation must be syntactically correct as per Python standards.
2.Clearly identify any fake or placeholder parameters used in the invocation.
3.Encourage generating a realistic and functional code snippet wherever possible.
4. If necessary, you can use the working directory provided by the user as a parameter passed into the __call__ method.
Now you will be provided with the following information, please generate your response according to these information:
'''
_LINUX_USER_INVOKE_GENERATOR_PROMPT = '''
User's Information:
Class Name: {class_name}
Task Description: {task_description}
__call__ Method Parameters: {args_description}
Working Directory: {working_dir}
'''


class LinuxInvokeGenerator():

    def __init__(self, config_path=None) -> None:
        super().__init__()
        self.llm = OpenAI(config_path)
        self.system_version = get_os_version()
        try:
            check_os_version(self.system_version)
        except ValueError as e:
            print(e)

    # Generate calls for the selected tool class
    def invoke_generator(self, class_code, task_description,working_dir):
        class_name, args_description = self.extract_class_name_and_args_description(class_code)
        self.sys_prompt = _LINUX_SYSTEM_INVOKE_GENERATOR_PROMPT
        self.user_prompt = _LINUX_USER_INVOKE_GENERATOR_PROMPT.format(
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
    
    # extract class_name and args description from python code
    def extract_class_name_and_args_description(self, class_code):
        """
        Extracts the class name and comments from the __call__ method of a given Python class code.
        Specifically extracts the class name and the content between 'Args:' and 'Returns:' in the __call__ method.

        Args:
            class_code (str): The string representation of the Python class code.

        Returns:
            tuple: A tuple containing the class name and the extracted comments between 'Args:' and 'Returns:', 
                or None for each if not found.
        """
        # # Extracting the class name
        # class_name_pattern = re.compile(r'class\s+(\w+)')
        # class_name_match = class_name_pattern.search(class_code)
        # class_name = class_name_match.group(1) if class_name_match else None

        # # Pattern to match __call__ method and its docstring
        # call_method_pattern = re.compile(r'def __call__\s*\(self, .*?\):\s*"""(.*?)"""', re.DOTALL)
        # call_method_match = call_method_pattern.search(class_code)

        # if call_method_match:
        #     docstring = call_method_match.group(1)
        #     # Extracting the part between Args: and Returns:
        #     args_to_return_pattern = re.compile(r'Args:(.*?)Returns:', re.DOTALL)
        #     args_to_return_match = args_to_return_pattern.search(docstring)

        #     call_args_comments = args_to_return_match.group(1).strip() if args_to_return_match else None
        # else:
        #     call_args_comments = None
        # Extracting the class name
        class_name_pattern = r"class (\w+)"
        class_name_match = re.search(class_name_pattern, class_code)
        class_name = class_name_match.group(1) if class_name_match else None

        # Extracting the __call__ method's docstring
        call_method_docstring_pattern = r"def __call__\([^)]*\):\s+\"\"\"(.*?)\"\"\""
        call_method_docstring_match = re.search(call_method_docstring_pattern, class_code, re.DOTALL)
        call_method_docstring = call_method_docstring_match.group(1).strip() if call_method_docstring_match else None

        return class_name, call_method_docstring

    

# class_code = '''
                       
# from jarvis.action.base_action import BaseAction
# import os

# class create_folder(BaseAction):
#     def __init__(self):
#         self._description = "Create a folder under the working directory"

#     def __call__(self, folder_name):
#         """
#         :param folder_name: The name of the folder to be created
#         """
#         # Change the current working directory to the specified path
#         os.chdir("/home/wengzhenmin/Projects/jarvis/working_dir")

#         # Create the folder
#         os.makedirs(folder_name)

# # Example usage:
# # create_folder_action = create_folder()
# # create_folder_action("test2")

# '''
# # task_description = '''
# # download music from the Internet to the DeskTop, and play it.
# # '''

# test = LinuxInvokeGenerator(config_path="../../examples/config.json")
# print(test.extract_class_name_and_args_description(class_code))

# file_path = 'invoke.txt'
# res = test.invoke_generator(class_code, task_description)
# with open(file_path, 'w', encoding='utf-8') as file:
#     file.write(res)
