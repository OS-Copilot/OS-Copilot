
from jarvis.action.base_action import BaseAction
import os

class retrieve_document(BaseAction):
    def __init__(self):
        self._description = "Search for .txt files containing a specific keyword within a designated folder and log their paths."

    def __call__(self, keyword="agent", folder_name="document", working_dir=None, *args, **kwargs):
        """
        Search for text files in the specified folder that contain the given keyword and log their full paths to a file.

        Args:
            keyword (str): The keyword to search for within text files. Defaults to "agent".
            folder_name (str): The name of the folder to search within. Defaults to "document".
            working_dir (str): The working directory where the folder is located. If not provided, uses the current working directory.

        Returns:
            None: This method does not return anything but writes the paths of matching files to 'agent.txt'.
        """
        # Set the working directory to the provided path or the current working directory
        if working_dir is None:
            working_dir = os.getcwd()

        # The path to the folder where the search will be performed
        search_path = os.path.join(working_dir, folder_name)

        # The file to which the paths of the matching text files will be written
        output_file_path = os.path.join(working_dir, 'agent.txt')

        # Check if the output file already exists and if so, rename it to avoid overwriting
        if os.path.exists(output_file_path):
            base, extension = os.path.splitext(output_file_path)
            i = 1
            new_output_file_path = f"{base}_{i}{extension}"
            while os.path.exists(new_output_file_path):
                i += 1
                new_output_file_path = f"{base}_{i}{extension}"
            output_file_path = new_output_file_path

        # Initialize the output file
        with open(output_file_path, 'w') as output_file:
            # Walk through the directory
            for root, dirs, files in os.walk(search_path):
                for file in files:
                    # Check if the file is a .txt file
                    if file.endswith('.txt'):
                        file_path = os.path.join(root, file)
                        # Open and read the file to search for the keyword
                        with open(file_path, 'r') as f:
                            contents = f.read()
                            # If the keyword is found, write the file's full path to the output file
                            if keyword in contents:
                                output_file.write(file_path + '\n')

        print("Task execution complete: Paths of text files containing the keyword have been logged to 'agent.txt'.")

# Example of how to use the class (this should be in comments):
# retriever = retrieve_document()
# retriever(keyword="agent", folder_name="document", working_dir="/home/heroding/桌面/Jarvis/working_dir")
