from jarvis.action.get_os_version import get_os_version, check_os_version
from jarvis.core.llms import OpenAI
from jarvis.agent.prompt import prompt_dict
import re
import json


class LinuxSkillCreateAgent():
    """
    LinuxSkillCreateAgent is used to generate new skills in Linux environment and store them in the action_lib.
    """    
    def __init__(self, config_path=None) -> None:
        super().__init__()
        self.llm = OpenAI(config_path)
        self.system_version = get_os_version()
        self.prompt = prompt_dict
        try:
            check_os_version(self.system_version)
        except ValueError as e:
            print(e)
    
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
    def invoke_generate_format_message(self, class_code, task_description):
        class_name, args_description = self.extract_class_name_and_args_description(class_code)
        self.sys_prompt = self.prompt['_LINUX_SYSTEM_INVOKE_GENERATE_PROMPT']
        self.user_prompt = self.prompt['_LINUX_USER_INVOKE_GENERATE_PROMPT'].format(
           class_name = class_name,
           task_description = task_description,
           args_description = args_description 
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
        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        print(judge_json)
        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
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
        """
        Extracts the class name and comments from the __call__ method of a given Python class code.
        Specifically extracts the class name and the content between 'Args:' and 'Returns:' in the __call__ method.

        Args:
            class_code (str): The string representation of the Python class code.

        Returns:
            tuple: A tuple containing the class name and the extracted comments between 'Args:' and 'Returns:', 
                or None for each if not found.
        """
        class_name_pattern = r"class (\w+)"
        class_name_match = re.search(class_name_pattern, class_code)
        class_name = class_name_match.group(1) if class_name_match else None

        # Extracting the __call__ method's docstring
        call_method_docstring_pattern = r"def __call__\([^)]*\):\s+\"\"\"(.*?)\"\"\""
        call_method_docstring_match = re.search(call_method_docstring_pattern, class_code, re.DOTALL)
        call_method_docstring = call_method_docstring_match.group(1).strip() if call_method_docstring_match else None

        return class_name, call_method_docstring
    
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
    