from jarvis.action.base_action import BaseAction
import subprocess
import os

class open_text_file(BaseAction):
    def __init__(self):
        self._description = "Open the specified text file in the specified folder using the default text viewer on Ubuntu."

    def __call__(self, folder_name, file_name, working_directory=None):
        """
        Open the specified text file in the specified folder using the default text viewer on Ubuntu.

        Args:
        folder_name (str): The name of the folder containing the text file.
        file_name (str): The name of the text file to be opened.
        working_directory (str, optional): The working directory where the folder is located. If not provided, the current working directory will be used.

        Returns:
        None
        """
        # If the working directory is provided, use it. Otherwise, use the current working directory.
        if working_directory:
            os.chdir(working_directory)

        # Construct the file path
        file_path = os.path.join(folder_name, file_name)

        # Open the text file using the default text viewer on Ubuntu
        subprocess.run(['xdg-open', file_path])

# Example of how to use the class:
# open_file_task = open_text_file()
# open_file_task(folder_name='myfold', file_name='result.txt', working_directory='/home/heroding/桌面/Jarvis/working_dir')
