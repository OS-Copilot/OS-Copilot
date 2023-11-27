from jarvis.action.get_os_version import get_os_version, check_os_version
from jarvis.core.llms import OpenAI

_LINUX_SYSTEM_PROMPT = '''
You are a helpful assistant that writes python code to complete any task specified by me.
System Version: {system_version}
Task: {task}
You should only respond in the format as described below:

from jarvis.action.base_action import BaseAction

class open_document(BaseAction):
    def __init__(self) -> None:
        super().__init__()
        self._description = ""

    # function __call__ is used to execute 
    def __call__(self, *args, **kwargs):
        # TODO: 




task_name()
'''
_LINUX_SYSTEM_PROMPT = '''
You are helpful assistant to assist in writing Python tool code for tasks completed on Linux operating systems. Your expertise lies in creating Python classes that perform specific tasks, adhering to a predefined format and structure.
Your goal is to generate Python tool code in the form of a class. The code should be structured to perform a user-specified task on a Linux operating system. The class must be easy to use and understand, with clear instructions and comments.

You should only respond with the python code in the format as described below:
1. Code Structure: Begin with the necessary import statement: from jarvis.action.base_action import BaseAction. Then, define the class using the task name provided by the user, converting it into a valid Python class name by replacing spaces with underscores.
2. Parameter Handling: In the __init__ method, only initialize self._description with a brief description of the class's purpose, detailing what task it accomplishes.
3. Subprocess Integration: If the task involves Linux bash operations, instruct the use of the subprocess library, particularly the run method, to execute these operations. This approach should be encapsulated within the __call__ method of the class.
4. Detailed Comments: Provide comprehensive comments throughout the code. This includes describing the purpose of the class, the usage of each method, and the function of parameters, especially in the __call__ method. End with an example of how to use the class, like open_document()(parameters).
And the code you write should also follow the following criteria:
1.The class must start with from jarvis.action.base_action import BaseAction.
2.The class name should be formatted based on the user's task name, with underscores separating different words. Please make the first letter of each word lowercase.
3.In the __init__ method, only self._description should be initialized.
4.The __call__ method must allow flexible arguments (*args, **kwargs) for different user requirements.
5.For tasks involving Linux bash commands, use the subprocess library to execute these commands within the Python class.
6.The code should include detailed comments explaining the purpose of the class, the role of each parameter, and a clear example of how to use the class.
7. If downloading a file is involved, the file name must follow the underscore (_) format to prevent garbled characters in the name.
Now you will be provided with the following two information:
System Version: {system_version}
Task: {task}
System language: simplified chinese
Please write python code to accomplish the task and be compatible with system environments, versions and language. The path names of the system may be inconsistent in different system languages.
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


skillCreator = LinuxSkillCreator(config_path="../../examples/config.json")
task = "Please download the audio I have given link from the Internet to the desktop of the system and play it in the system."
python_code = skillCreator.format_message(task)
if '```python' in python_code:
    python_code = python_code.split('```python')[1].split('```')[0]
elif '```' in python_code:
    python_code = python_code.split('```')[1].split('```')[0]
file_name = "my_python_script.py"

# 打开文件并写入代码字符串
with open(file_name, "w") as file:
    file.write(python_code)

print(f"The Python code has been saved to {file_name}")
