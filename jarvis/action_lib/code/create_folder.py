from jarvis.action.base_action import BaseAction
import os

class create_folder(BaseAction):
    def __init__(self):
        self._description = "Create a folder under the default working directory."

    def __call__(self, working_directory=None, folder_name='myfold', *args, **kwargs):
        """
        Create a folder under the specified working directory or the default working directory.

        Args:
        working_directory (str): The path of the working directory. If not provided, the default working directory will be used.
        folder_name (str): The name of the folder to be created. Default is 'myfold'.

        Returns:
        None
        """
        # Check if the working_directory is provided, if not, use the default working directory
        if working_directory:
            os.chdir(working_directory)

        # Create the folder
        os.makedirs(folder_name)

# Example of how to use the class
# create_folder_action = create_folder()
# create_folder_action(working_directory='/home/heroding/桌面/Jarvis/working_dir', folder_name='my_new_folder')
