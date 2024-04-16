import pytest
from oscopilot.utils import setup_config
from oscopilot import FridayPlanner, ToolManager
from oscopilot.prompts.friday_pt import prompt

class TestPlanner:
    """
    A test class for verifying the functionality of the FridayPlanner class.
    
    This class focuses on testing the task decomposition capabilities of the planner, ensuring that tasks
    can be broken down into subtasks effectively. It is crucial for validating that the planner properly
    interprets and decomposes high-level tasks into actionable steps.
    """    
    def setup_method(self, method):
        """
        Setup method executed before each test method in this class.
        
        This method prepares the FridayPlanner instance by configuring it with necessary settings and a predefined
        planning prompt, ensuring that the planner is ready to handle task decomposition.

        Args:
            method: The test method that will be run after this setup method. While this parameter is not used
                    directly in the setup, it is included to comply with the expected signature for setup methods
                    in the testing framework.
        """        
        args = setup_config()
        self.prompt = prompt["planning_prompt"]
        self.planner = FridayPlanner(self.prompt)

    def test_decompose_task(self):
        """
        Test to verify that the task decomposition process in the FridayPlanner does not result in an empty subtask list.

        This test checks the functionality of the `decompose_task` method by providing a specific task description
        and ensuring that the planner is capable of breaking it down into one or more subtasks. An empty list of
        subtasks would indicate a failure in the decomposition process, which is critical for the planner's utility
        in real-world applications.

        """        
        task, tool_description_pair = "Install pandas package", ""
        self.planner.decompose_task(task, tool_description_pair)
        assert self.planner.sub_task_list != []

if __name__ == '__main__':
    pytest.main()
    
    
