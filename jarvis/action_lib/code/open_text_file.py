
from jarvis.action.base_action import BaseAction
import subprocess
import os

class open_text_file(BaseAction):
    def __init__(self):
        self._description = "Open the specified text file using the default text viewer on the system."

    def __call__(self, file_path, *args, **kwargs):
        """
        Open the specified text file using the default text viewer on the system.

        Args:
        file_path (str): The absolute path of the text file to be opened.

        Returns:
        None
        """
        # Ensure the file exists before attempting to open it
        if not os.path.isfile(file_path):
            print(f"The file {file_path} does not exist.")
            return

        # Open the text file using the default text viewer on Ubuntu
        try:
            subprocess.run(['xdg-open', file_path])
            print(f"Opened the file {file_path} successfully.")
        except Exception as e:
            print(f"An error occurred while trying to open the file: {e}")

# Example of how to use the class:
# open_file_task = open_text_file()
# open_file_task(file_path='/home/heroding/桌面/Jarvis/working_dir/test.txt')
