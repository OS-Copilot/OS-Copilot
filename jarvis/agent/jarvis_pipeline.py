from jarvis.agent.linux_skill_creator import LinuxSkillCreator
from jarvis.agent.linux_skill_amend import LinuxSkillAmend
from jarvis.agent.openai_agent import OpenAIAgent
from jarvis.enviroment.py_env import PythonEnv

environment = PythonEnv()
agent = OpenAIAgent(config_path="../../examples/config.json")
skill_amend = LinuxSkillAmend(config_path="../../examples/config.json")


response = '''
Thought: To download a file from internet , we can focus on xxx.

Actions: 
1. <action>download_and_play_music</action>

Check local action_lib, the required action code is in the library, according to the function description in the code, combined with the information provided by the user, You can instantiate classes for different tasks.

invoke:
1. <invoke>download_and_play_music()("https://dasex101-random-learning.oss-cn-shanghai.aliyuncs.com/DataEthics/Taylor%20Swift%20-%20Look%20What%20You%20Made%20Me%20Do.mp3")</invoke>
'''

action = agent.extract_action(response, begin_str='<action>', end_str='</action>')
invoke = agent.extract_invoke(response, begin_str='<invoke>', end_str='</invoke>')
task = "Download audio from a given link and play it on the system."

for (i, a) in enumerate(action):
    command = agent.action_lib[a] + '\n' + invoke[i]
    res = environment.step(command)
    times = 0
    # Test skill_amend and check the output in txt file.
    # if res.error != None:
    #     new_code = skill_amend.amend_code(command, task, res.error)
    #     path = "new_code.txt"
    #     with open(path, 'w', encoding='utf-8') as file:
    #         file.write(new_code)

    # Loop through code fixes until there are no errors or the number of fixes is exceeded.        
    while res.error != None and times < 3:
        new_code = skill_amend.amend_code(command, task, res.error)
        if '```python' in new_code:
            new_code = new_code.split('```python')[1].split('```')[0]
        elif '```' in new_code:
            new_code = new_code.split('```')[1].split('```')[0]
        command = new_code + '\n' + invoke[i]
        res = environment.step(command)
        times = times + 1

    # TODO: If the code runs correctly, save the code to action_lib, otherwise the user will be prompted that the task cannot be executed.
    