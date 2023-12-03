from jarvis.action.base_action import BaseAction
import os
import shutil

class organize_document(BaseAction):
    def __init__(self):
        self._description = "This class organizes retrieved files into a folder named agent, with the file paths listed in a txt file named agent."

    def __call__(self, file_path, working_directory=None):
        """
        Organize retrieved files into a folder named agent, with the file paths listed in a txt file named agent.

        Args:
        file_path (str): The path of the txt file containing the retrieved file paths.
        working_directory (str, optional): The working directory path. If not provided, the current working directory will be used.

        Returns:
        None
        """
        # Set the working directory
        if working_directory:
            os.chdir(working_directory)
        
        # Create the folder named agent
        os.makedirs("agent", exist_ok=True)

        # Read the txt file and move the files to the agent folder
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                file_path = line.strip()
                if os.path.exists(file_path):
                    file_name = os.path.basename(file_path)
                    shutil.move(file_path, os.path.join("agent", file_name))
                else:
                    print(f"File not found: {file_path}")

# Example of how to use the class:
# org_doc = organize_document()
# org_doc(file_path="retrieved_files.txt", working_directory="/home/heroding/桌面/Jarvis/working_dir")
