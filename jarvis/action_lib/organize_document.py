from jarvis.action.base_action import BaseAction
import os
import shutil

class organize_document(BaseAction):
    def __init__(self):
        self._description = "This class organizes the retrieved files into a folder named agent, with the file paths listed in a txt file named agent."

    def __call__(self, working_directory, file_list_path):
        """
        This method organizes the retrieved files into a folder named agent, with the file paths listed in a txt file named agent.

        Args:
        working_directory (str): The working directory where the files will be organized.
        file_list_path (str): The path to the txt file containing the list of file paths.

        Returns:
        None
        """
        # Change the current working directory to the specified working directory
        os.chdir(working_directory)

        # Create the folder named agent if it doesn't exist
        agent_folder = os.path.join(working_directory, 'agent')
        if not os.path.exists(agent_folder):
            os.makedirs(agent_folder)

        # Read the file paths from the txt file
        with open(file_list_path, 'r', encoding='utf-8') as file:
            file_paths = file.read().splitlines()

        # Move the retrieved files into the agent folder
        for file_path in file_paths:
            file_name = os.path.basename(file_path)
            destination_path = os.path.join(agent_folder, file_name)
            shutil.move(file_path, destination_path)
