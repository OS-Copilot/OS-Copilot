
from jarvis.action.base_action import BaseAction
import json
import os

class extract_jsonl_content(BaseAction):
    def __init__(self):
        self._description = "Extract the full text content of the specified JSON Lines file."

    def __call__(self, jsonl_file_path, *args, **kwargs):
        """
        Extract the full text content of the specified JSON Lines file and return its content.

        Args:
            jsonl_file_path (str): The absolute path to the JSON Lines file to be read.

        Returns:
            list: A list of dictionaries, each representing a line in the JSON Lines file.
        """
        try:
            # Change the current working directory to the specified path if provided
            working_dir = kwargs.get('working_dir', os.getcwd())
            os.chdir(working_dir)

            # Ensure the JSON Lines file exists
            if not os.path.isfile(jsonl_file_path):
                print(f"The JSON Lines file {jsonl_file_path} does not exist.")
                return

            # Read the JSON Lines file
            content = []
            with open(jsonl_file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    content.append(json.loads(line.strip()))

            print(f"Task execution complete. Content of the JSON Lines file {jsonl_file_path} extracted successfully.")
            return content
        except FileNotFoundError:
            print(f"The JSON Lines file {jsonl_file_path} does not exist.")
        except json.JSONDecodeError as e:
            print(f"An error occurred while parsing the JSON Lines file {jsonl_file_path}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

# Example of how to use the class (this should be in the comments):
# extractor = extract_jsonl_content()
# content = extractor(jsonl_file_path='/home/heroding/桌面/Jarvis/working_dir/2023_validation_metadata.jsonl')
