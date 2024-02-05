from action.get_os_version import get_os_version, check_os_version
from jarvis.core.llms import OpenAI

_MAC_SYSTEM_PROMPT = '''
You are a helpful assistant that writes AppleScript code to complete any task specified by me.
System Version: {system_version}
Task: {task}
You should only respond in the format as described below:

import subprocess

def task_name():
    # <task description>
    applescript = f"""
    <Code Completion>
    """
    subprocess.run(["osascript", "-e", applescript])

task_name()
'''

_LINUX_SYSTEM_PROMPT = '''
You are a helpful assistant that writes Python code to complete any task specified by me.
I will give you the following informations:
System Version: {system_version}
Task: {task}
You should only respond in the format as described below:

from jarvis.action.base_action import BaseAction

# TODO: you should write a class in the following format, and the class name should be the same as the task name,besides,you can design the parameters of __call__ as you want.
class task_name(BaseAction):
    def __init__(self) -> None:
        super().__init__()
        # self._description should be initialized as the description of the task
        self._description = ""
        # self.action_type should be initialized as the type of the task, which can be 'BASH' or 'PYTHON'
        self.action_type = ''

    def __call__(self, *args):
        # TODO: write your code here



'''


class SkillCreator():
    """
    SkillCreator is used to generate new skills and store them in the action_lib.
    """
    def __init__(self, config_path=None) -> None:
        super().__init__()
        self.llm = OpenAI(config_path)
        self.system_version = get_os_version()
        try:
            check_os_version(self.system_version)
        except ValueError as e:
            print(e)
        # self.mac_systom_prompts = 

    def format_message(self, task):
        self.prompt = _MAC_SYSTEM_PROMPT.format(
            system_version=self.system_version,
            task=task
        )
        self.message = [
            {"role": "system", "content": self.prompt},
            {"role": "user", "content": task},
        ]
        return self.llm.chat(self.message)

        