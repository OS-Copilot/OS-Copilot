from jarvis.action.get_os_version import get_os_version, check_os_version
from jarvis.core.llms import OpenAI
from prompt import prompt_dict


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
    
    def format_message(self, task_name,task_description,working_dir):
        self.sys_prompt = self.prompt[_LINUX_SYSTEM_SKILL_CREATE_PROMPT]
        self.user_prompt = self.prompt[_LINUX_USER_SKILL_CREATE_PROMPT].format(
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
        
    def extract_python_code(self, response):
        python_code = ""
        if '```python' in response:
            python_code = response.split('```python')[1].split('```')[0]
        elif '```' in python_code:
            python_code = response.split('```')[1].split('```')[0]
        return python_code    
