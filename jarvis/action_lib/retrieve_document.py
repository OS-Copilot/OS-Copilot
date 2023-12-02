from jarvis.action.base_action import BaseAction
import os
import subprocess

class retrieve_document(BaseAction):
    def __init__(self):
        self._description = "Search for the txt text in the document folder and save the full path of the text containing the word 'agent' in agent.txt."

    def __call__(self, working_directory):
        """
        Search for the txt text in the document folder and save the full path of the text containing the word 'agent' in agent.txt.

        Args:
        working_directory (str): The working directory where the document folder is located.

        Returns:
        None
        """
        # Change the current working directory to the specified working directory
        os.chdir(working_directory)

        # Create a list to store the full paths of the text files containing the word 'agent'
        agent_files = []

        # List all the files in the document folder
        document_folder = os.path.join(working_directory, "document")
        files = os.listdir(document_folder)

        # Iterate through the files and check for the word 'agent'
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(document_folder, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if 'agent' in content:
                        agent_files.append(file_path)

        # Write the full paths of the text files containing the word 'agent' to agent.txt
        with open('agent.txt', 'w', encoding='utf-8') as agent_file:
            for file_path in agent_files:
                agent_file.write(file_path + '\n')
