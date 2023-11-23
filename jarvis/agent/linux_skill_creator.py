from action.get_os_version import get_os_version, check_os_version
from jarvis.core.llms import OpenAI

_LINUX_SYSTEM_PROMPT = '''
You are a helpful assistant that writes python code to complete any task specified by me.
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


class LinuxSkillCreator():
    """
    LinuxSkillCreator is used to generate new skills in Linux environment and store them in the action_lib.
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
        self.prompt = _LINUX_SYSTEM_PROMPT.format(
            system_version=self.system_version,
            task=task
        )
        self.message = [
            {"role": "system", "content": self.prompt},
            {"role": "user", "content": task},
        ]
        return self.llm.chat(self.message)

        