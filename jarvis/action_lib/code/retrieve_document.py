
from jarvis.action.base_action import BaseAction
import os

class retrieve_document(BaseAction):
    def __init__(self):
        self._description = "Search for a txt document in the 'document' folder within the working directory, and if the document contains the word 'agent', save its full path to agent.txt."

    def __call__(self, working_directory=None):
        """
        Search for a txt document in the 'document' folder within the working directory, and if the document contains the word 'agent', save its full path to agent.txt.

        Args:
        working_directory (str): The path to the working directory. If not provided, the current working directory will be used.

        Returns:
        None
        """
        # Set the working directory
        if working_directory:
            os.chdir(working_directory)
        else:
            working_directory = os.getcwd()

        # Define the folder and file names
        folder_name = "document"
        search_word = "agent"
        output_file = "agent.txt"

        # Check if the document folder exists
        if os.path.exists(folder_name) and os.path.isdir(folder_name):
            # Iterate through the files in the document folder
            for root, dirs, files in os.walk(folder_name):
                for file in files:
                    if file.endswith(".txt"):
                        file_path = os.path.join(root, file)
                        # Search for the word 'agent' in the document
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            if search_word in content:
                                # Save the full path of the document to agent.txt
                                with open(output_file, 'a', encoding='utf-8') as output:
                                    output.write(file_path + '\n')
        else:
            print(f"The '{folder_name}' folder does not exist in the working directory.")

# Example of how to use the class:
# retrieve = retrieve_document()
# retrieve(working_directory="/home/heroding/桌面/Jarvis/working_dir")
