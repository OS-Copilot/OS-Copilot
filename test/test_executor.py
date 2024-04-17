import pytest
from oscopilot.utils import setup_config
from oscopilot import FridayExecutor, ToolManager
from oscopilot.prompts.friday_pt import prompt

class TestExecutor:
    """
    A test class for verifying the functionality of the FridayExecutor class.
    
    This class tests the code generation capabilities of the executor, particularly how it handles the creation
    of tool invocations based on specified task requirements. The tests are designed to ensure the output from
    the executor's methods is correctly formatted and non-empty.
    """    

    def setup_method(self, method):
        """
        Setup method executed before each test method in this class.
        
        This method initializes the FridayExecutor with a configuration and a predefined prompt for execution,
        setting the stage for subsequent tests. This setup is crucial for ensuring that the executor is configured
        properly with the necessary context and tool management capabilities before performing any tests.

        Args:
            method: The test method that will be run after this setup method. This parameter isn't directly used
                    but reflects the test framework's capability to pass the test method as an argument if needed.
        """        
        args = setup_config()
        self.prompt = prompt["execute_prompt"]
        self.executor = FridayExecutor(self.prompt, ToolManager)

    def test_generator_tool(self):
        """
        Test to ensure that the code generation by the FridayExecutor returns valid and non-empty outputs.

        This test assesses the `generate_tool` method of the executor by providing it with a specific task name,
        task description, and additional context (though empty in this case) to see if the resulting code and
        invoke command are correctly populated and not empty. This is crucial for validating that the executor
        can effectively translate task descriptions into actionable code snippets and commands.

        """
        task_name, task_description, pre_tasks_info, relevant_code = "move_files", "Move any text file located in the working_dir/document directory that contains the word 'agent' to a new folder named 'agent' ", "", ""
        code, invoke = self.executor.generate_tool(task_name, task_description, pre_tasks_info, relevant_code)
        assert [code, invoke] != ['', '']

if __name__ == '__main__':
    pytest.main()
    