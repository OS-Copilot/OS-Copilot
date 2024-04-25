from oscopilot.utils import setup_config
from oscopilot import BasicPlanner, ToolManager
from oscopilot.prompts.friday2_pt import prompt


args = setup_config()
prompt = prompt["planning_prompt"]
planner = BasicPlanner(prompt)
task = "Copy any text file located in the working_dir/document directory that contains the word 'agent' to a new folder named 'agents'"
planner.decompose_task(task)