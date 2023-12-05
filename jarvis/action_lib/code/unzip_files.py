from jarvis.action.base_action import BaseAction
import os
import zipfile

class unzip_files(BaseAction):
    def __init__(self):
        self._description = "Unzip test2.zip in the folder called test2 to the folder called test."

    def __call__(self, *args, **kwargs):
        # Get the working directory from the user-provided information
        working_dir = "/home/heroding/桌面/Jarvis/working_dir"

        # Change the current working directory to the specified working directory
        os.chdir(working_dir)

        # Define the source zip file and the destination folder
        source_zip = "test2/test2.zip"
        destination_folder = "test"

        # Unzip the files
        with zipfile.ZipFile(source_zip, 'r') as zip_ref:
            zip_ref.extractall(destination_folder)

# Example of how to use the class:
# unzip_task = unzip_files()
# unzip_task()
