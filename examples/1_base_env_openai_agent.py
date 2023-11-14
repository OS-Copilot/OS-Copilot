from jarvis.agent.openai_agent import OpenAIAgent
from jarvis.enviroment.old_env import BaseEnviroment

'''
A minimal example for base env and openai agent
The goal of this example is to demonstrate how agent parse response to get actions, and env execute those actions.
'''

environment = BaseEnviroment()
agent = OpenAIAgent(config_path="config.json")

response = '''
Thought: To set up the working environment, we can focus on two sub-goals: turning on dark mode and organizing the app layout.

Actions: 
1. <action>turn_on_dark_mode</action>
2. <action>turn_on_light_mode</action>'''

action = agent.extract_action(response, begin_str='<action>', end_str='</action>')
import time
for a in action:
    command = agent.action_lib[a]
    print(a, command)
    print(environment.step(command))
    time.sleep(2)