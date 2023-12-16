from jarvis.agent.openai_agent import OpenAIAgent
from jarvis.environment.py_env import PythonEnv
from jarvis.agent.jarvis_agent import ExecutionModule, JarvisAgent

'''
Made By DZC & WZM
target: Classify files in a specified folder.
'''

# path of action lib
action_lib_path = "../jarvis/action_lib"

# use to create new skills
jarvis_agent = JarvisAgent(config_path="./config.json", action_lib_dir=action_lib_path)
planning_agent = jarvis_agent.planner


task = '''Create the dzc.txt file in the working directory and write "dzc" into the file.'''
planning_agent.decompose_task(task)

# print(planning_agent.extract_json_from_string('''```json
# {
#     "reasoning": "The provided code defines a class 'retrieve_document' that inherits from 'BaseAction'. The '__call__' method of this class is designed to search for .txt files containing a specific keyword within a designated folder and log their paths to a file named 'agent.txt'. The code sets the working directory, searches for .txt files containing the keyword, and writes the paths of matching files to 'agent.txt'. The code output indicates that the task was executed and the paths were written to the specified file in the working directory. The presence of 'agent.txt' in the working directory, as shown in the provided files and folders list, suggests that the file was successfully created. The task description matches the code's functionality, and the code output confirms that the task was completed as intended.",
#     "judge": true,
#     "score": 7
# }
# ```'''
# ))