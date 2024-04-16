import pytest
from oscopilot.utils import SheetTaskLoader, get_project_root_path

class TestSheetTaskLoader:
    """
    A test class for verifying the functionality of the SheetTaskLoader class.
    
    This class includes methods to set up test conditions, and test various functionalities such as converting
    tasks to queries, loading the dataset of sheet tasks, and retrieving specific tasks by ID.
    """
    
    def setup_method(self, method):
        """
        Setup method executed before each test method in this class.
        
        This method prepares a SheetTaskLoader instance using a predetermined path to the sheet tasks JSONL file,
        effectively setting the environment for subsequent tests.

        Args:
            method: The test method that will be run after this setup method. This parameter isn't directly used
                    but reflects the test framework's capability to pass the test method as an argument if needed.
        """
        sheet_task_path = get_project_root_path() + "examples/SheetCopilot/sheet_task.jsonl"
        self.sheet_task_loader = SheetTaskLoader(sheet_task_path)

    def test_task2query(self):
        """
        Test to ensure that converting a task to a query does not return an empty string.

        This test calls the `task2query` method of the SheetTaskLoader with mock parameters and checks if the result
        is not an empty string, indicating that the method is functioning correctly and producing output.
        """        
        assert self.sheet_task_loader.task2query("context.", "instructions.", "file_path") != ""


    def test_load_sheet_task_dataset(self):
        """
        Test to ensure that loading the sheet task dataset does not return an empty list.

        This test verifies that the `load_sheet_task_dataset` method is capable of loading data and the result is
        a non-empty list, suggesting that the dataset contains entries.
        """
        assert self.sheet_task_loader.load_sheet_task_dataset() != []

    def test_get_task_by_id(self):
        """
        Test to ensure that retrieving a task by its ID does not return an empty dictionary.

        This test confirms that the `get_data_by_task_id` method returns a dictionary with content when queried with
        a valid task ID, which in this case, is presumed to be 1.
        """        
        assert self.sheet_task_loader.get_data_by_task_id(1) != {}

if __name__ == '__main__':
    pytest.main()

