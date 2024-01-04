
from jarvis.action.base_action import BaseAction
import os

class read_layout_file(BaseAction):
    def __init__(self):
        self._description = "Read the content of a specified text file."

    def __call__(self, file_path, *args, **kwargs):
        """
        Read the content of the specified text file and return its content.

        Args:
            file_path (str): The absolute path to the text file to be read.

        Returns:
            str: The content of the text file.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            print(f"Task execution complete. Content of the file {file_path} read successfully.")
            return content
        except FileNotFoundError:
            print(f"The file {file_path} does not exist.")
        except Exception as e:
            print(f"An error occurred while reading the file {file_path}: {e}")

# Example of how to use the class (this should be in the comments):
# reader = read_layout_file()
# content = reader(file_path='/home/heroding/.cache/huggingface/datasets/downloads/70a1ee0ae9b188db8f50a933dc95ce2e1cd3cbe2d015c7b4bd91444f003db5fd.txt')
