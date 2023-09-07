import copy
import io
import json
import os
import time

import requests

from utils.api_service import chat_gpt
from utils.file import *
from utils.config_manager import ConfigManager

config_manager = ConfigManager()
os.environ['OPENAI_API_KEY'] = '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'  # $5
config_manager.clear_proxies()

# os.environ["http_proxy"] = "http://127.0.0.1:10809"
# os.environ["https_proxy"] = "http://127.0.0.1:10809"


def action(action_str):
    try:
        print(f'action={action_str}')
        result = eval(action_str)
        return result
    except SyntaxError as e:
        return f"Give me the complete action."
    except Exception as e:
        return f"An error occurred: {e}"


def get_content(s, begin_str='[BEGIN]', end_str='[END]'):
    result = []
    _begin = s.find(begin_str)
    _end = s.find(end_str)
    while not (_begin == -1 or _end == -1):
        result.append(s[_begin + len(begin_str):_end].strip())
        s = s[_end + len(end_str):]
        _begin = s.find(begin_str)
        _end = s.find(end_str)
    return result


system_prompt = '''You are a personal assistant that aims to automate the workflow for human. 
You are capable of understanding human intent and decompose it into several subgoals that can be addressed via language generation or acomplished using external tools. 
Some of the external tools you can use and their functionalities are as follows:
Tool 1: <action>turn_on_dark_mode()</action>
Using turn_on_dark_mode() will change your system into the dark mode.
The dark mode is good for focused study and no-distraction time.
Tool 2: <action>play_study_music()</action> 
Using play_study_music()  will open Music in your Mac and play songs that are sutiable for study and work.
Tool 3: <action>create_meeting()</action> 
Using create_meeting() will help user create a meeting event.  
When users request to create a meeting, don't ask questions such as meeting title and time, just invoke this tool by generating <action>create_meeting()</action>.
Tool 4: <action>show_upcoming_meetings()</action> 
Using show_upcoming_meetings() will open Calendar and show the their upcoming meetings for the user.
Tool 5: <action>organize_app_layout()</action>
Using organize_app_layout() will help user reorganize their Desktop layout for better working condition and focus more easily.
Remember you must surround you action between <action> and </action>).
'''

base_url = 'http://localhost:12345'

def turn_on_dark_mode():
    command = 'shortcuts run "Dark Mode"'
    response = requests.post(f'{base_url}/tools/shell', data=json.dumps({"command": command}), headers={'Content-Type': 'application/json'})
    if response.status_code == 200:
        # print("Command executed successfully")
        # print("STDOUT: ", response.json()['stdout'])
        # print("STDERR: ", response.json()['stderr'])
        return "succefully changed the system into dark mode, happy studying!"
    else:
        print("Error occurred while executing the command")

def play_study_music():
    command = 'shortcuts run "Play Playlist"'
    response = requests.post(f'{base_url}/tools/shell', data=json.dumps({"command": command}), headers={'Content-Type': 'application/json'})
    if response.status_code == 200:
        return "succefully played songs in the playlist: Work, happy studying!"
    else:
        return "Error occurred while playing music"

def organize_app_layout():
    command = 'shortcuts run "Organize APP Layout"'
    response = requests.post(f'{base_url}/tools/shell', data=json.dumps({"command": command}), headers={'Content-Type': 'application/json'})
    if response.status_code == 200:
        return "succefully splite the screen into two"
    else:
        return "Error occurred while activate app and split screen."

def create_meeting():
    command = 'shortcuts run "Create Meeting in Calendar"'
    response = requests.post(f'{base_url}/tools/shell', data=json.dumps({"command": command}), headers={'Content-Type': 'application/json'})
    if response.status_code == 200:
        return "succefully add meeting!"
    else:
        return "Error occurred while creating calendar"

def show_upcoming_meetings():
    command = 'shortcuts run "Show Upcoming Meeting in Calendar"'
    response = requests.post(f'{base_url}/tools/shell', data=json.dumps({"command": command}),
                             headers={'Content-Type': 'application/json'})
    if response.status_code == 200:
        print("STDOUT: ", response.json()['stdout'])
        print("STDERR: ", response.json()['stderr'])
        return "succefully open calendar!"
    else:
        return "Error occurred while creating calendar"


max_iter = 10
model_name="gpt-3.5-turbo-16k"

# turn_on_dark_mode()
# play_study_music()

study = "I want to start working now. Please help set up the working environment for me."
show_cal = "Please show me my upcoming meetings"
create_cal = "Please create a meeting "

highliht_thought = "\033[31m{}\033[0m"
highliht_action = "\033[34m{}\033[0m"
highliht_user = "\033[32m{}\033[0m"
while True:
# for prompt in [study, show_cal, create_cal]:
    prompt = input(highliht_user.format("User:\t"))
    messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ]
    print(highliht_user.format("User:\t"+prompt))
    response = chat_gpt(messages=messages, sleep_time=2, model_name=model_name)

    # print(f'response={response}')
    messages.append(response)
    pred = response['content']
    print(highliht_thought.format("Thought:\t"+pred))
    action_strs = get_content(pred, begin_str='<action>', end_str='</action>')
    # print(f'actions={action_strs}')
    # if len(action_strs) > 0 and 'over()' in action_strs:
    #     messages.append({"role": "user",
    #                      "content": f"{summary_prompt}"})
    #     print(f'\n\nover()\n\n')
    action_result = ""
    action_id = int(input(highliht_user.format("Input the action you want to execute:\t")))
    while True and action_id <= len(action_strs):
        action_str = action_strs[action_id]
        print(highliht_action.format("Action:\t" + action_str))
        # time.sleep(5)
        print(action(action_str))
        # for action_str in action_strs:

            # action_result +=
            # print(f'action_result={action_result}')
