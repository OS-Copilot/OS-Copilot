from friday.action.get_os_version import get_os_version, check_os_version
from friday.core.llms import OpenAI
import json
_LINUX_SYSTEM_Judger_PROMPT = '''
You are an AI programmed to verify Python code against a user's task requirements.
Your goal is to determine if the provided Python code accomplishes the user's specified task based on the feedback information.
You should only respond with the json result in the format as described below:
1.Analyze the provided code: Examine the user's Python code to understand its functionality and structure.
2.Compare the code with the task description: Align the objectives stated in the user's task description with the capabilities of the code.
3.Evaluate the feedback information: Review the user's feedback, including the output of the code and any file changes or directory states, to gauge the code's effectiveness.
4.Formulate a reasoning process: Synthesize the analysis, comparison, and evaluation to create a logical reasoning process about the code's effectiveness in achieving the task.
5.Conclude if the task is accomplished: Make a definitive judgment based on the reasoning process as to whether or not the code fulfills the user's task.
7.Output Format: You should only return me a json with no extra content. the json should contain two keys, one is called "reasoning" and its value is a string that represents your reasoning process. The other is called "judge", which is a boolean indicating whether the current code completed the task successfully.
And you should also follow the following criteria:
1.Ensure accurate understanding of the Python code.
2.Relate the code functionality to the user's task.
3.Assess the feedback information for evidence of task completion.
4.Provide clear, logical reasoning.
5.You need to note that the code I gave you is not reporting errors, I just don't know if it actually accomplishes the task or not.
6.Information about the current working directory and all the files and folders under it may imply whether the file was created successfully or not.
Now you will be provided with the following information, please give the result json according to these information:
'''
_LINUX_USER_Judger_PROMPT = '''
User's information are as follows:
Current Code: {current_code}
Task: {task}
Code Output: {code_output}
Current Working Directiory: {working_dir}
Files And Folders in Current Working Directiory: {files_and_folders}
'''


class LinuxTaskJudger():

    def __init__(self, config_path=None) -> None:
        super().__init__()
        self.llm = OpenAI(config_path)
        self.system_version = get_os_version()
        try:
            check_os_version(self.system_version)
        except ValueError as e:
            print(e)

    # amend the code to fullfill the task.
    def judge(self, current_code,task,code_output,working_dir,files_and_folders):
        self.sys_prompt = _LINUX_SYSTEM_Judger_PROMPT
        self.user_prompt = _LINUX_USER_Judger_PROMPT.format(
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
        judge_json = json.loads(response)
        return judge_json

# judger = LinuxTaskJudger(config_path="../../examples/config.json")
# current_code='''
# from friday.action.base_action import BaseAction
# import os

# class create_folder(BaseAction):
#     def __init__(self):
#         self._description = "Create a folder under the working directory"

#     def __call__(self, *args, **kwargs):
#         # Get the working directory
#         working_dir = os.getcwd()

#         # Create the folder path
#         folder_name = "ss"
#         folder_path = os.path.join(working_dir, folder_name)

#         # Check if the folder already exists
#         if os.path.exists(folder_path):
#             print(f"The folder '{folder_name}' already exists.")
#         else:
#             # Create the folder
#             os.makedirs(folder_path)
#             print(f"The folder '{folder_name}' has been created under the working directory.")

# # Example usage
# # create_folder_action = create_folder()
# # create_folder_action()

# '''
# task="create a folder which is named test2 under the working directory"
# code_output =""
# working_dir ="/home/wengzhenmin/Projects/friday/working_dir"
# files_and_folders ="ss\n"
# res = judger.judge(current_code=current_code,code_output=code_output,task=task,working_dir=working_dir,files_and_folders=files_and_folders)
# print(res)
# print(res["judge"])