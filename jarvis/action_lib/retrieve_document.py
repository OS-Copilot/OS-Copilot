from jarvis.action.base_action import BaseAction
import os

class retrieve_document(BaseAction):
    def __init__(self):
        self._description = "Search the txt text in the folder called document in the working directory. If the text contains the word 'agent', put the full path of the text into agent.txt and wrap it in a new line."

    def __call__(self, working_directory):
        """
        Search for txt files in the 'document' folder within the specified working directory.
        If the text contains the word 'agent', the full path of the text is added to agent.txt and wrapped in a new line.

        Args:
        working_directory (str): The path to the working directory.

        Returns:
        None
        """
        # Change the current working directory to the specified working directory
        os.chdir(working_directory)

        # Create a list to store the paths of the txt files containing the word 'agent'
        agent_files = []

        # Iterate through the 'document' folder to find txt files
        for root, dirs, files in os.walk('document'):
            for file in files:
                if file.endswith(".txt"):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if 'agent' in content:
                            agent_files.append(file_path)

        # Write the paths of the txt files containing the word 'agent' to agent.txt
        with open('agent.txt', 'w', encoding='utf-8') as agent_file:
            for file_path in agent_files:
                agent_file.write(file_path + '\n')
