from jarvis.action.base_action import BaseAction
import os

class create_text_file_and_write_something(BaseAction):
    def __init__(self):
        self._description = "Create a text file and write something in it."

    def __call__(self, working_directory, folder_name, file_name, content):
        """
        Create a text file and write something in it.

        Args:
        working_directory (str): The working directory where the folder and file will be created.
        folder_name (str): The name of the folder where the file will be created.
        file_name (str): The name of the text file to be created.
        content (str): The content to be written in the text file.

        Returns:
        None
        """
        # Change the current working directory to the specified working directory
        os.chdir(working_directory)

        # Create the folder if it doesn't exist
        folder_path = os.path.join(working_directory, folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Create and write to the text file
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'w') as file:
            file.write(content)

# Example of how to use the class
# create_text_file_and_write_something_instance = create_text_file_and_write_something()
# create_text_file_and_write_something_instance(working_directory='/home/heroding/桌面/Jarvis/working_dir', folder_name='myfold', file_name='result.txt', content='hello world')
