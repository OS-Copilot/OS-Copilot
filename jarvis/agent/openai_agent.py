import json
from jarvis.core.llms import OpenAI
from jarvis.agent.base_agent import BaseAgent
from jarvis.enviroment.old_env import BaseEnviroment
from jarvis.core.schema import EnvState


a = "{action_input} the input to the action, could be any valid input for python programs or shell commands, such numbers, strings, or path to a file, etc."
BASE_PROMPT = """
{system_prompt}
{tool_description}
To use a tool, please use the following format:
```
{thought} to address the user request, thinking about what are the sub-goals you need to achieve and which tool is needed for each sub-goal?
{action} the tool names, each action name should be one of [{action_names}]. 
```
The response after utilizing tools should using the following format:
```
{response} To generate a response, you need to summarize your thoughts above and combined them with the tool execution results.
``
If you already know the answer, or you do not need to use tools,
please using the following format to reply:
```
{thought} the thought process to answer user questions
{response} respond to user request based on thought
```
Remember you must surround you action between <action> and </action>.
Now you are ready to take questions and requests from users.
"""


class OpenAIAgent(BaseAgent):
    """
    BaseAgent is the base class of all agents.
    """
    def __init__(self, config_path=None):
        super().__init__()
        self.llm = OpenAI(config_path)
        self.actions = None
        self.max_iter = 10
        self.system_prompt = """You are a personal assistant that aims to automate the workflow for human.\nYou are capable of understanding human intent and decompose it into several subgoals that can be addressed via language generation or acomplished using external tools.\nSome of the external tools you can use and their functionalities are as follows:
        """
        self.action_names = self.action_lib.keys()
        # todo: 添加工具检索模块
        self.available_action_description = ""
        for i, name in enumerate(self.action_names):
            self.available_action_description += "Tool {}: <action>{}</action>\n{}\n".format(i+1, name, self.action_lib_description[name])

    def from_config(self, config_path=None):
        self.llm = OpenAI(config_path)

    def format_message(self, query):
        self.prompt = BASE_PROMPT.format(
            system_prompt=self.system_prompt,
            tool_description=self.available_action_description,
            action_names=self.action_names,
            thought="Thought:",
            action="Actions:",
            action_input="Action Input:",
            response="Response:"
        )
        self.message = [
            {"role": "system", "content": self.prompt},
            {"role": "user", "content": query},
        ]
        return self.llm.chat(self.message)

    def extract_action(self, message, begin_str='[BEGIN]', end_str='[END]'):
        result = []
        _begin = message.find(begin_str)
        _end = message.find(end_str)
        while not (_begin == -1 or _end == -1):
            result.append(message[_begin + len(begin_str):_end].strip())
            message = message[_end + len(end_str):]
            _begin = message.find(begin_str)
            _end = message.find(end_str)
        return result
    
    def extract_invoke(self, message, begin_str='[BEGIN]', end_str='[END]'):
        result = []
        _begin = message.find(begin_str)
        _end = message.find(end_str)
        while not (_begin == -1 or _end == -1):
            result.append(message[_begin + len(begin_str):_end].strip())
            message = message[_end + len(end_str):]
            _begin = message.find(begin_str)
            _end = message.find(end_str)
        return result    

    # # @dzc
    # def extract_parameter(self, message, begin_str='[BEGIN]', end_str='[END]'):
    #     result = []
    #     _begin_parameter = message.find(begin_str)
    #     _end_parameter = message.find(end_str)
    #     # go through parameters
    #     while not (_begin_parameter == -1 or _end_parameter == -1):
    #         # get current task parameters
    #         parameter = message[_begin_parameter + len(begin_str):_end_parameter].strip()
    #         _begin_arg = parameter.find("<arg>")
    #         _end_arg = parameter.find("</arg>")
    #         args = []
    #         # go through args
    #         while not (_begin_arg == -1 or _end_arg == -1): 
    #             arg = parameter[_begin_arg + len("<arg>"): _end_arg].strip()
    #             args.append(arg)
    #             parameter = parameter[_end_arg + len("</arg>"):].strip()
    #             _begin_arg = parameter.find("<arg>")
    #             _end_arg = parameter.find("</arg>")
    #         result.append(args)
    #         message = message[_end_parameter + len(end_str):]
    #         _begin_parameter = message.find(begin_str)
    #         _end_parameter = message.find(end_str)
    #     return result

    def chat(self, goal: str):
        self._history = []

    def step(self, single_action) -> EnvState:
        _command = self.action_lib[single_action]
        self.environment.step(_command)
        return self.environment.observe()


if __name__ == '__main__':
    actions = {
        "turn_on_dark_mode()": "Using turn_on_dark_mode() will change your system into the dark mode.",
        "play_study_music()": "Using play_study_music()  will open Music in your Mac and play songs that are sutiable for study and work.",
        "create_meeting()": "Using create_meeting() will help user create a meeting event. When users request to create a meeting, don't ask questions such as meeting title and time, just invoke this tool by generating the action name.",
        "show_upcoming_meetings()": "Using show_upcoming_meetings() will open Calendar and show the their upcoming meetings for the user.",
        "organize_app_layout()": "Using organize_app_layout() will help user reorganize their Desktop layout for better working condition and focus more easily."
    }
    environment = BaseEnviroment()
    agent = OpenAIAgent(config_path="../../examples/config.json", environment=environment)

    # print(agent.action_lib)
    # print(agent.action_lib_description)
    # executation_action = agent.action_lib["turn_on_dark_mode"]()
    # executation_action.run()
    # response = agent.format_message(query="I want to start working now. Please help set up the working environment for me.")
    # print(agent.prompt)
    # print(response['content'])
    response = '''
Thought: To set up the working environment, we can focus on two sub-goals: turning on dark mode and organizing the app layout.

Actions: 
1. <action>turn_on_dark_mode</action>
2. <action>turn_on_light_mode</action>'''
    action = agent.extract_action(response, begin_str='<action>', end_str='</action>')
    import time
    for a in action:
        print(a)
        command = agent.action_lib[a]
        print(agent.env.step(command))
        time.sleep(2)