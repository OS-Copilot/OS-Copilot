
from jarvis.action.base_action import BaseAction
import os

class read_text_file(BaseAction):
    def __init__(self):
        self._description = "Read the full text content of a specified text file."

    def __call__(self, file_path, *args, **kwargs):
        """
        Read the content of the specified text file and return its content.

        Args:
            file_path (str): The absolute path to the text file to be read.

        Returns:
            str: The content of the text file, or None if an error occurs.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            print(f"Task execution complete. Content of the file {file_path} read successfully.")
            return content
        except FileNotFoundError:
            print(f"The file {file_path} does not exist.")
            return None
        except Exception as e:
            print(f"An error occurred while reading the file {file_path}: {e}")
            return None

# Example of how to use the class (this should be in the comments):
# reader = read_text_file()
# content = reader(file_path='/home/heroding/.cache/huggingface/datasets/downloads/90d142b33359cd5fba1aa1ac9be83cd48d112baf51a675fc08e26d5b1d5c0402.txt')
