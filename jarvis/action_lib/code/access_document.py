
from jarvis.action.base_action import BaseAction
import os

class access_document(BaseAction):
    def __init__(self):
        self._description = "Access the document located at the specified file path."

    def __call__(self, file_path, *args, **kwargs):
        """
        Access the document at the given file path and return its content if it's a file.

        Args:
            file_path (str): The absolute path to the document to be accessed.

        Returns:
            str: The content of the document if it's a file, or None if it's not a file.
        """
        try:
            if os.path.isfile(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                except UnicodeDecodeError:
                    with open(file_path, 'rb') as file:
                        content = file.read()
                print(f"Document accessed successfully at {file_path}.")
                return content
            else:
                print(f"The path {file_path} is not a file.")
                return None
        except FileNotFoundError:
            print(f"The file at {file_path} does not exist.")
            return None
        except Exception as e:
            print(f"An error occurred while accessing the file at {file_path}: {e}")
            return None
