import pytest
from oscopilot.utils import SheetTaskLoader, get_project_root_path

class TestSheetTaskLoader:
    def setup_method(self, method):
        sheet_task_path = get_project_root_path() + "examples/SheetCopilot/sheet_task.jsonl"
        self.sheet_task_loader = SheetTaskLoader(sheet_task_path)

    def test_task2query(self):
        assert self.sheet_task_loader.task2query("context.", "instructions.", "file_path") != ""


    def load_sheet_task_dataset(self):
        assert self.sheet_task_loader.load_sheet_task_dataset() != []

    def test_get_task_by_id(self):
        assert self.sheet_task_loader.get_data_by_task_id(1) != {}

if __name__ == '__main__':
    pytest.main()

