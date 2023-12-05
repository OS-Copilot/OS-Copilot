from jarvis.action.base_action import BaseAction
import os
import zipfile

class zip_files(BaseAction):
    def __init__(self):
        self._description = "Zip all the files in the specified folder"

    def __call__(self, folder_name):
        """
        Zip all the files in the specified folder and name the zip file as the folder name.

        Args:
        folder_name (str): The name of the folder containing the files to be zipped.

        Returns:
        None
        """
        try:
            # Get the current working directory
            current_dir = os.getcwd()

            # Change the current working directory to the specified folder
            os.chdir(folder_name)

            # Get the list of files in the folder
            file_list = os.listdir()

            # Create a zip file with the folder name
            with zipfile.ZipFile(f"{folder_name}.zip", "w") as zipf:
                # Add each file in the folder to the zip file
                for file in file_list:
                    zipf.write(file)

        except FileNotFoundError as e:
            print(f"Error: {e}")

        finally:
            # Change the working directory back to the original directory
            os.chdir(current_dir)
