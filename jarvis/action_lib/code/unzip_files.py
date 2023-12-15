
from jarvis.action.base_action import BaseAction
import os
import zipfile
import subprocess

class unzip_files(BaseAction):
    def __init__(self):
        self._description = "Unzip a specified .zip file into a designated folder."

    def __call__(self, zip_file_path, destination_folder, working_directory=None, *args, **kwargs):
        """
        Unzip the specified .zip file into the designated folder.

        Args:
            zip_file_path (str): The path to the .zip file to be unzipped.
            destination_folder (str): The folder where the .zip file contents will be extracted.
            working_directory (str, optional): The working directory where the operation will be performed.
                If not provided, the current working directory will be used.

        Returns:
            None
        """
        # If a working directory is provided, change to that directory
        if working_directory:
            os.chdir(working_directory)
        else:
            # Use the current working directory if none is provided
            working_directory = os.getcwd()

        # Ensure the destination folder exists
        destination_path = os.path.join(working_directory, destination_folder)
        os.makedirs(destination_path, exist_ok=True)

        # Unzip the file
        try:
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(destination_path)
            print(f"Unzipped {zip_file_path} into {destination_folder} successfully.")
        except zipfile.BadZipFile:
            print(f"Failed to unzip {zip_file_path}: The file may be corrupted or not a zip file.")
        except FileNotFoundError:
            print(f"Failed to unzip {zip_file_path}: The file does not exist.")

# Example of how to use the class (this should be in the comments and not executed):
# unzipper = unzip_files()
# unzipper(zip_file_path='agent.zip', destination_folder='myfold', working_directory='/home/heroding/桌面/Jarvis/working_dir')
