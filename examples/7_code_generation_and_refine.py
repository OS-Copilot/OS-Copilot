from jarvis.agent.openai_agent import OpenAIAgent
from jarvis.enviroment.py_env import PythonEnv
from jarvis.agent.linux_skill_creator import LinuxSkillCreator
from jarvis.agent.linux_skill_amend import LinuxSkillAmend
from jarvis.agent.linux_invoke_generator import LinuxInvokeGenerator
'''
Made By WZM & DZC
用处：jarvis工具代码生成pipeline
'''
environment = PythonEnv()
agent = OpenAIAgent(config_path="./config.json")
skillCreator = LinuxSkillCreator(config_path="./config.json")
invokeGenerator = LinuxInvokeGenerator(config_path="./config.json")

response = '''
Thought: To download a file from internet , we can focus on xxx.

Actions: 
1. <action>create_folder</action> <description>create a folder which is named test under the working directory</description>
2. <action>create_file</action> <description>create a txt file which is named sth.txt under a directory named test which is under the working directory.Then Write hello world in it.</description>
Check local action_lib, the required action code is in the library, according to the function description in the code, combined with the information provided by the user, You can instantiate classes for different tasks.

'''
action = agent.extract_action(response, begin_str='<action>', end_str='</action>')
task_description = agent.extract_action(response, begin_str='<description>', end_str='</description>')
for a,t in zip(action,task_description):
    print(environment.working_dir)
    msg = skillCreator.format_message(task_name=a,task_description=t,working_dir=environment.working_dir)
    code = skillCreator.extract_python_code(msg)
    msg_invoke = invokeGenerator.invoke_generator(code, t)
    invoke = agent.extract_action(msg_invoke, begin_str='<invoke>', end_str='</invoke>')[0]
    code = code + '\n' + invoke
    print(code)

    state = environment.step(code)
    print(state)