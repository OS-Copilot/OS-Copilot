from jarvis.action.base_action import BaseAction
import os
import shutil

class organize_document(BaseAction):
    def __init__(self):
        self._description = "This class organizes the retrieved files into a folder named agent, with the file paths placed in a txt file named agent.txt."

    def __call__(self, working_directory, file_list_path):
        """
        Organize the retrieved files into a folder named agent, with the file paths placed in a txt file named agent.txt.

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
            file_paths = file.readlines()
        
        # Remove any leading or trailing whitespaces from the file paths
        file_paths = [path.strip() for path in file_paths]

        # Move the files to the agent folder
        for path in file_paths:
            file_name = os.path.basename(path)
            destination_path = os.path.join(agent_folder, file_name)
            shutil.move(path, destination_path)

        # Create the agent.txt file with the updated file paths
        with open(os.path.join(working_directory, 'agent.txt'), 'w', encoding='utf-8') as file:
            for path in file_paths:
                file.write(path + '\n')