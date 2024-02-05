from friday.action.get_os_version import get_os_version, check_os_version
from friday.core.llms import OpenAI

_LINUX_SYSTEM_AMEND_PROMPT = '''
You are an AI expert in Python programming, with a focus on diagnosing and resolving code issues.
Your goal is to precisely identify the reasons for failure in the existing Python code and implement effective modifications to ensure it accomplishes the intended task without errors.

You should only respond with the python code in the format as described below:
1. Modified Code: Based on the error analysis, modify the original code to fix all the problems and give the final correct code to the user.
2. Error Analysis: Conduct a step-by-step analysis to identify why the code is generating errors or failing to complete the task. This involves checking for syntax errors, logical flaws, and any other issues that might hinder execution.
3. Detailed Explanation: Offer a clear and comprehensive explanation for each identified issue, detailing why these problems are occurring and how they are impacting the code's functionality.
And the code you write should also follow the following criteria:
1. You must keep the original code as formatted as possible, e.g. class names, methods, etc. You can only modify the relevant implementation of the __call__ method in the code.
2. Please avoid throwing exceptions in your modified code which may result in the execution of your code consistently reporting errors.You should instead handle the caught exceptions!
3. Some errors may be caused by unreasonable tasks by the user that result in something other than what is expected, e.g. the file to be created already exists, the parameters passed in are wrong, etc. You need to do some fault tolerance or exception handling for this to prevent it from reporting further errors.
4. Ensure the final code is syntactically correct, optimized for performance, and follows Python best practices.And the final code can only contain the class definition, the rest of the code about class instantiation and invocation must be commented out.
5. The python code should be surrounded by ```python and ```.
6. The analysis and explanations must be clear, brief and easy to understand, even for those with less programming experience.
7. All modifications must address the specific issues identified in the error analysis.
8. The solution must enable the code to successfully complete the intended task without errors.
Now you will be provided with the following information, please give your modified python code according to these information:
'''
_LINUX_USER_AMEND_PROMPT = '''
User's information are as follows:
Original Code: {original_code}
Task: {task}
Error Messages: {error}
Code Output: {code_output}
Current Working Directiory: {working_dir}
Files And Folders in Current Working Directiory: {files_and_folders}
Critique On The Code: {critique}
'''


class LinuxSkillAmend():

    def __init__(self, config_path=None) -> None:
        super().__init__()
        self.llm = OpenAI(config_path)
        self.system_version = get_os_version()
        try:
            check_os_version(self.system_version)
        except ValueError as e:
            print(e)

    # amend the code to fullfill the task.
    def amend_code(self, original_code, task, error,code_output,working_dir,files_and_folders,critique):
        self.sys_prompt = _LINUX_SYSTEM_AMEND_PROMPT
        self.user_prompt = _LINUX_USER_AMEND_PROMPT.format(
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
    def extract_python_code(self, response):
        python_code = ""
        if '```python' in response:
            python_code = response.split('```python')[1].split('```')[0]
        elif '```' in python_code:
            python_code = response.split('```')[1].split('```')[0]
        return python_code
