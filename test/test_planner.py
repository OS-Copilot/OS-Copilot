import pytest
from oscopilot.utils import setup_config
from oscopilot import FridayPlanner, ToolManager
from oscopilot.prompts.friday_pt_new import prompt

class TestPlanner:
    def setup_method(self, method):
        args = setup_config()
        self.prompt = prompt["planning_prompt"]
        self.planner = FridayPlanner(self.prompt)

    def test_decompose_task(self):
        task, tool_description_pair = "Install pandas package", ""
        self.planner.decompose_task(task, tool_description_pair)
        assert self.planner.sub_task_list != []

if __name__ == '__main__':
    pytest.main()
    
    
