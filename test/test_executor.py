import pytest
from oscopilot.utils import setup_config
from oscopilot import FridayExecutor, ToolManager
from oscopilot.prompts.friday_pt_new import prompt

class TestExecutor:
    def setup_method(self, method):
        args = setup_config()
        self.prompt = prompt["execute_prompt"]
        self.executor = FridayExecutor(self.prompt, ToolManager)

    def test_generator_tool(self):
        task_name, task_description, pre_tasks_info, relevant_code = "move_files", "Move any text file located in the working_dir/document directory that contains the word 'agent' to a new folder named 'agent' ", "", ""
        code, invoke = self.executor.generate_tool(task_name, task_description, pre_tasks_info, relevant_code)
        assert [code, invoke] != ['', '']

if __name__ == '__main__':
    pytest.main()
    