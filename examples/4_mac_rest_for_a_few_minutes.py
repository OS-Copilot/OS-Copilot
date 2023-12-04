from jarvis.agent.openai_agent import OpenAIAgent
from jarvis.agent.skill_creator import SkillCreator
# from jarvis.enviroment.old_env import BaseEnviroment
from jarvis.enviroment.bash_env import BashEnv
from jarvis.enviroment.py_env import PythonEnv

'''
A minimal example for creating new skills
'''

# environment = BaseEnviroment()
environment = PythonEnv()
agent = OpenAIAgent(config_path="examples/config.json")
skill_creator = SkillCreator(config_path="examples/config.json")

response = '''
Thought: Taking a 20-minute break means we can focus on the following three sub-tasks: 1. Enable Do Not Disturb mode; 2. Play some light music; 3. Set a 20-minute alarm.

Actions: 
0. <action>set_30_minute_alarm</action>
1. <action>enable_do_not_disturb</action>
2. <action>play_light_music</action>
3. <action>set_20_minute_alarm</action>'''

action = agent.extract_action(response, begin_str='<action>', end_str='</action>')
import time
for a in action:
    if a in agent.action_lib:
        command = agent.action_lib[a]
        print("Successfully read the '{}' command from the action lib.".format(a))
    else:
        print("There is no '{}' command in the action lib and a new one needs to be created.".format(a))
        response = skill_creator.format_message(a)
        print(response)


    print(a, command)
    print(environment.step(command))
    time.sleep(2)