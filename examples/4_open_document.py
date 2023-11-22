from jarvis.agent.openai_agent import OpenAIAgent
from jarvis.enviroment.py_env import PythonEnv

'''
A minimal example for base env and openai agent
The goal of this example is to demonstrate how agent parse response to get actions, and env execute those actions.
'''

environment = PythonEnv()
agent = OpenAIAgent(config_path="config.json")

response = '''
Thought: To open a document named , we can focus on one goal: open the specified document(word, pdf, pptx, txt etc.).

Actions: 
1. <action>open_document</action>

Check local action_lib, the required action code is in the library, according to the function description in the code, combined with the information provided by the user, You can instantiate classes for different tasks.

invoke:
1. <invoke>open_document()("/home/heroding/桌面/rnn.pptx" , "pptx")</invoke>
'''

action = agent.extract_action(response, begin_str='<action>', end_str='</action>')
invoke = agent.extract_invoke(response, begin_str='<invoke>', end_str='</invoke>')

for (i, a) in enumerate(action):
    command = agent.action_lib[a] + "\n" + invoke[i]
    # print(command)
    print(environment.step(command))
