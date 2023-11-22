from jarvis.agent.openai_agent import OpenAIAgent
from jarvis.enviroment.old_env import BaseEnviroment
from jarvis.enviroment.py_env import PythonEnv
from jarvis.enviroment.bash_env import BashEnv
'''
Made By WZM
用处：查看指定区域这几天的天气
'''

# environment = BaseEnviroment()
environment = PythonEnv()
agent = OpenAIAgent(config_path="config.json")

response = '''
Thought: To set up the working environment, we can focus on two sub-goals: turning on dark mode and organizing the app layout.

Actions: 
1. <action>check_weather</action> <invoke>check_weather()("shanghai","putuo")</invoke>

'''

action = agent.extract_action(response, begin_str='<action>', end_str='</action>')
invoke = agent.extract_action(response, begin_str='<invoke>', end_str='</invoke>')
print(invoke)
import time
for (i,a) in enumerate(action):
    command = agent.action_lib[a] + "\n" + invoke[i]
    # print(a, command)
    print(environment.step(command).result)
    # time.sleep(2)

# from jarvis.action_lib.execute_sql import execute_sql as ExecuteSQL

# action = ExecuteSQL()
# action(query='SELECT * FROM railway\nWHERE number="D1000";')
