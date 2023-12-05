
from jarvis.action.base_action import BaseAction
import os
import shutil

class organize_document(BaseAction):
    def __init__(self):
        self._description = "This class organizes the retrieved files into a folder named agent, with the file paths listed in the agent.txt file."

    def __call__(self, working_directory, agent_txt_path):
        """
        Args:
        working_directory (str): The working directory where the retrieved files and agent.txt file are located.
        agent_txt_path (str): The path to the agent.txt file containing the paths of the retrieved files.
        Returns:
        None
        """
        # Change the current working directory to the specified working directory
        os.chdir(working_directory)

        # Create the folder named agent if it does not exist
        agent_folder_path = os.path.join(working_directory, 'agent')
        if not os.path.exists(agent_folder_path):
            os.makedirs(agent_folder_path)

        # Read the agent.txt file to retrieve the file paths
        with open(agent_txt_path, 'r', encoding='utf-8') as file:
            file_paths = file.read().splitlines()

        # Move the retrieved files to the agent folder
        for file_path in file_paths:
            file_name = os.path.basename(file_path)
            destination_path = os.path.join(agent_folder_path, file_name)
            shutil.move(file_path, destination_path)
