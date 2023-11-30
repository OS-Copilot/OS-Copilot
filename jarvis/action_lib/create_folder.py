from jarvis.action.base_action import BaseAction
import os

class create_folder(BaseAction):
    def __init__(self):
        self._description = "This class creates a folder under the default working directory."

    def __call__(self, folder_name):
        """
        Create a folder under the default working directory.

        Args:
        folder_name (str): The name of the folder to be created.

        Returns:
        None
        """
        # Change the current working directory to the specified path
        os.chdir('/home/heroding/桌面/Jarvis/working_dir')

        # Create the folder
        os.makedirs(folder_name)

# Example of how to use the class:
# create_folder_action = create_folder()
# create_folder_action("test2")
