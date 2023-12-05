from jarvis.action.base_action import BaseAction
import os

class retrieve_document(BaseAction):
    def __init__(self):
        self._description = "Search for a txt document in the 'document' folder within the working directory, and if the document contains the word 'agent', save its full path to agent.txt."

    def __call__(self, working_directory=None):
        """
        Args:
        working_directory (str): The path to the working directory. If not provided, the current working directory will be used.
        
        Returns:
        None
        """
        # Set the working directory
        if working_directory:
            os.chdir(working_directory)
        
        # Define the folder and file names
        folder_name = "document"
        search_word = "agent"
        output_file = "agent.txt"
        
        # Check if the document folder exists
        if os.path.exists(folder_name) and os.path.isdir(folder_name):
            # Change the working directory to the document folder
            os.chdir(folder_name)
            
            # Search for txt files containing the search word
            agent_files = [file for file in os.listdir() if file.endswith(".txt") and search_word in open(file).read()]
            
            # Write the full path of the agent files to agent.txt
            with open(output_file, "w") as f:
                for file in agent_files:
                    f.write(os.path.abspath(file) + "\n")
        else:
            print(f"The '{folder_name}' folder does not exist in the working directory.")