from jarvis.agent.openai_agent import OpenAIAgent
from jarvis.enviroment.old_env import BaseEnviroment

'''
A minimal example for base env and openai agent
The goal of this example is to demonstrate how agent parse response to get actions, and env execute those actions.
'''

environment = BaseEnviroment()
agent = OpenAIAgent(config_path="config.json")

response = '''
Thought: To open a document, we can focus on one goal: open the specified document(word, pdf, pptx, txt).

Actions: 
1. <action>open_document</action>
Paramters:
1. <parameter><arg>path:/home/heroding/桌面/test.txt</arg><arg>name:test.txt</arg><arg>type:txt</arg></parameter>
'''

action = agent.extract_action(response, begin_str='<action>', end_str='</action>')
paramter = agent.extract_parameter(response, begin_str='<parameter>', end_str='</parameter>')
print(paramter)
# import time
# for a in action:
#     command = agent.action_lib[a]
#     # print(a, command)
#     print(environment.step(command))
#     # time.sleep(2)

# from jarvis.action_lib.execute_sql import ExecuteSQL

# action = ExecuteSQL()
# action(query='SELECT * FROM railway\nWHERE number="D1000";')
