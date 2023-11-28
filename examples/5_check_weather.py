from jarvis.agent.openai_agent import OpenAIAgent
from jarvis.enviroment.old_env import BaseEnviroment
from jarvis.enviroment.py_env import PythonEnv
from jarvis.enviroment.bash_env import BashEnv
import time
'''
Made By WZM
用处：查看指定区域这几天的天气
'''

# environment = BaseEnviroment()
environment = PythonEnv()
agent = OpenAIAgent(config_path="examples/config.json")

response = '''
Thought: To set up the working environment, we can focus on two sub-goals: turning on dark mode and organizing the app layout.

Actions: 
1. <action>check_weather</action> <invoke>check_weather()("shanghai","putuo")</invoke>

'''

action = agent.extract_action(response, begin_str='<action>', end_str='</action>')
invoke = agent.extract_action(response, begin_str='<invoke>', end_str='</invoke>')

for (i,a) in enumerate(action):
    command = agent.action_lib[a] + "\n" + invoke[i]
    print(environment.step(command).result)

