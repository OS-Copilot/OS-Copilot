from jarvis.action.base_action import BaseAction
import os

class retrieve_document(BaseAction):
    def __init__(self):
        self._description = "Search for the txt files in the 'document' folder within the working directory, and if the file contains the word 'agent', save the full path of the file in agent.txt."

    def __call__(self, working_directory=None):
        """
        Search for the txt files in the 'document' folder within the working directory, and if the file contains the word 'agent', save the full path of the file in agent.txt.

        Args:
        working_directory (str): The path of the working directory. If not provided, the current working directory will be used.

        Returns:
        None
        """
        # Set the working directory
        if working_directory:
            os.chdir(working_directory)
        else:
            working_directory = os.getcwd()

        # Define the folder name
        folder_name = "document"

        # Create a list to store the paths of the txt files containing the word "agent"
        agent_files = []

        # Iterate through the files in the document folder
        for root, dirs, files in os.walk(folder_name):
            for file in files:
                if file.endswith(".txt"):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if "agent" in content:
                            agent_files.append(file_path)

        # Write the paths of the agent files to agent.txt
        with open("agent.txt", 'w', encoding='utf-8') as agent_file:
            for file_path in agent_files:
                agent_file.write(file_path + "\n")
