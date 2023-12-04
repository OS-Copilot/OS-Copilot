from jarvis.agent.openai_agent import OpenAIAgent
from jarvis.enviroment.py_env import PythonEnv

'''
Made By DZC
The function is to be able to open any type of document.
'''

environment = PythonEnv()
agent = OpenAIAgent(config_path="examples/config.json")

response = '''
Thought: To open a document named , we can focus on one goal: open the specified document(word, pdf, pptx, txt etc.).

Actions: 
1. <action>open_document</action> <invoke>open_document()("/Users/hanchengcheng/Desktop/云大合作重点研发计划/国家版本典藏资源数字化服务关键技术与平台研发-重点研发计划申报书.pdf")</invoke>

invoke:
1. <invoke>open_document()("/home/heroding/桌面/rnn.pptx" , "pptx")</invoke>
'''

action = agent.extract_action(response, begin_str='<action>', end_str='</action>')
invoke = agent.extract_invoke(response, begin_str='<invoke>', end_str='</invoke>')

for (i, a) in enumerate(action):
    command = agent.action_lib[a] + "\n" + invoke[i]
    print(environment.step(command).result)
