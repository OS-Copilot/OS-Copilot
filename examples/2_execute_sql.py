from jarvis.agent.openai_agent import OpenAIAgent
from jarvis.enviroment.old_env import BaseEnviroment
from jarvis.enviroment.py_env import PythonEnv

'''
A minimal example for base env and openai agent
The goal of this example is to demonstrate how agent parse response to get actions, and env execute those actions.
'''

# environment = BaseEnviroment()
environment = PythonEnv()
agent = OpenAIAgent(config_path="config.json")

response = '''
Thought: To set up the working environment, we can focus on two sub-goals: turning on dark mode and organizing the app layout.

Actions: 
1. <action>execute_sql</action>'''

action = agent.extract_action(response, begin_str='<action>', end_str='</action>')
import time
for a in action:
    command = agent.action_lib[a] + '\nprint({tool_name}()())'.format(tool_name=a)
    # print(a, command)
    print(environment.step(command).result)
    # time.sleep(2)

# from jarvis.action_lib.execute_sql import ExecuteSQL

# action = ExecuteSQL()
# action(query='SELECT * FROM railway\nWHERE number="D1000";')
