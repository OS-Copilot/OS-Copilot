from jarvis.agent.openai_agent import OpenAIAgent
from jarvis.enviroment.base_env import BaseEnviroment

'''
A minimal example for base env and openai agent
The goal of this example is to demonstrate how agent parse response to get actions, and env execute those actions.
'''

environment = BaseEnviroment()
agent = OpenAIAgent(config_path="config.json")

response = '''
Thought: To set up the working environment, we can focus on two sub-goals: turning on dark mode and organizing the app layout.

Actions: 
1. <action>execute_sql</action>'''

action = agent.extract_action(response, begin_str='<action>', end_str='</action>')
import time
for a in action:
    command = agent.action_lib[a]
    # print(a, command)
    print(environment.step(command))
    # time.sleep(2)

from jarvis.action_lib.execute_sql import execute_sql

action = execute_sql()
action.run(db_path='../tasks/travel/database/travel.db',
           query='SELECT * FROM railway\nWHERE number="D1000";')
