from jarvis.action.base_action import BaseAction
import os
import shutil

class organize_document(BaseAction):
    def __init__(self):
        self._description = "This class organizes the retrieved files into a folder named agent, with the file paths listed in a txt file named agent."

    def __call__(self, file_path, working_directory=None):
        """
        Organize the retrieved files into a folder named agent, with the file paths listed in a txt file named agent.

        Args:
        file_path (str): The path of the txt file containing the list of file paths.
        working_directory (str, optional): The working directory where the files will be organized. If not provided, the current working directory will be used.

        Returns:
        None
        """
        # Set the working directory
        if working_directory:
            os.chdir(working_directory)
        
        # Create the folder named agent
        os.makedirs("agent", exist_ok=True)

        # Read the file paths from the txt file
        with open(file_path, 'r', encoding='utf-8') as file:
            file_paths = file.read().splitlines()

        # Move the files to the agent folder
        for path in file_paths:
            file_name = os.path.basename(path)
            shutil.move(path, os.path.join("agent", file_name))
