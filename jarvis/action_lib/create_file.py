from jarvis.action.base_action import BaseAction
import os

class create_file(BaseAction):
    def __init__(self):
        self._description = "Create a txt file under a directory and write 'hello world' in it."

    def __call__(self, *args, **kwargs):
        # Get the working directory from the user's information
        working_directory = '/home/heroding/桌面/Jarvis/working_dir'

        # Create the full path for the directory and the file
        directory_path = os.path.join(working_directory, 'test2')
        file_path = os.path.join(directory_path, 'sth2.txt')

        # Change the current working directory to the specified path
        os.chdir(working_directory)

        # Create the directory if it doesn't exist
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

        # Write 'hello world' to the file
        with open(file_path, 'w') as file:
            file.write('hello world')

        return f"File sth2.txt created under directory test2 in the working directory."
