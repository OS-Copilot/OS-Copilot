from oscopilot import FridayExecutor, ToolManager, FridayPlanner
from oscopilot.prompts.friday_pt import prompt
from oscopilot.utils import setup_config

args = setup_config()
# prompt = prompt["execute_prompt"]
# excutor = FridayExecutor(prompt, ToolManager)
# task_name, task_description, pre_tasks_info, relevant_code = "move_files", "Move any text file located in the working_dir/document directory that contains the word 'agent' to a new folder named 'agent' ", "", ""
# code, invoke = excutor.generate_tool(task_name, task_description, pre_tasks_info, relevant_code)
# print(code, '\n', invoke)

prompt = prompt["planning_prompt"]
planner = FridayPlanner(prompt)
task, tool_description_pair = "Install pandas package", ""
planner.decompose_task(task, tool_description_pair)

