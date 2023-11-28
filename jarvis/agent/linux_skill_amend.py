from jarvis.action.get_os_version import get_os_version, check_os_version
from jarvis.core.llms import OpenAI

_LINUX_SYSTEM_AMEND_PROMPT = '''
You are an AI expert in Python programming, with a focus on diagnosing and resolving code issues.
Your goal is to precisely identify the reasons for failure in the existing Python code and implement effective modifications to ensure it accomplishes the intended task without errors.

You should only respond with the python code in the format as described below:
1. Initial Code Review: Begin by examining the provided Python code. Gain an understanding of its purpose, structure, and the logic it employs to accomplish the task.
2. Error Analysis: Conduct a step-by-step analysis to identify why the code is generating errors or failing to complete the task. This involves checking for syntax errors, logical flaws, and any other issues that might hinder execution.
3. Detailed Explanation: Offer a clear and comprehensive explanation for each identified issue, detailing why these problems are occurring and how they are impacting the code's functionality.
4. Solution Development: Based on the error analysis, suggest specific changes to rectify the issues. This could include syntax corrections, logic adjustments, or structural optimizations to improve performance.
5. Code Testing and Validation: Describe how to test the modified code to ensure that it now meets the task requirements and is free from the previously identified issues.
6. Programming Best Practices: Provide additional tips or best practices in Python programming that are relevant to the issues encountered, helping to prevent similar problems in future coding endeavors.
And the code you write should also follow the following criteria:
1. The analysis and explanations must be clear, detailed, and easy to understand, even for those with less programming experience.
2. All modifications must address the specific issues identified in the error analysis.
3. Ensure the final code is syntactically correct, optimized for performance, and follows Python best practices.
4. The solution must enable the code to successfully complete the intended task without errors.
Now you will be provided with the following information, please modify the original python code to fix all the problems according to these information:
'''
_LINUX_USER_AMEND_PROMPT = '''
User's information are as follows:
Original Code: {original_code}
Task: {task}
Error Messages: {error}
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
    def amend_code(self, original_code, task, error):
        self.sys_prompt = _LINUX_SYSTEM_AMEND_PROMPT
        self.user_prompt = _LINUX_USER_AMEND_PROMPT.format(
           original_code = original_code,
           task = task,
           error = error 
        )
        self.message = [
            {"role": "system", "content": self.sys_prompt},
            {"role": "user", "content": self.user_prompt},
        ]
        return self.llm.chat(self.message)
