from jarvis.agent.openai_agent import OpenAIAgent
from jarvis.enviroment.py_env import PythonEnv

'''
Made By DZC
The function is to install environment missing package.
'''

environment = PythonEnv()
agent = OpenAIAgent(config_path="config.json")

response = '''
Thought: To  install environment missing package , we can focus on one goal: run "pip install xxx" in Bash.

Actions: 
1. <action>install_package</action>

Check local action_lib, the required action code is in the library, according to the function description in the code, combined with the information provided by the user, You can instantiate classes for different tasks.

invoke:
1. <invoke>install_package()("numpy")</invoke>
'''

action = agent.extract_action(response, begin_str='<action>', end_str='</action>')
invoke = agent.extract_invoke(response, begin_str='<invoke>', end_str='</invoke>')

for (i, a) in enumerate(action):
    command = agent.action_lib[a] + "\n" + invoke[i]
    print(environment.step(command))
