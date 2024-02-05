
from jarvis.action.base_action import BaseAction
import json
import os

class read_json_file(BaseAction):
    def __init__(self):
        self._description = "Read the content of the specified JSON file."

    def __call__(self, json_file_path, *args, **kwargs):
        """
        Read the content of the specified JSON file and return its content.

        Args:
            json_file_path (str): The absolute path to the JSON file to be read.

        Returns:
            dict: The content of the JSON file.
        """
        try:
            # Ensure the JSON file exists
            if not os.path.isfile(json_file_path):
                print(f"The JSON file {json_file_path} does not exist.")
                return

            # Read the JSON file
            with open(json_file_path, 'r', encoding='utf-8') as file:
                content = json.load(file)

            print(f"Task execution complete. Content of the JSON file {json_file_path} read successfully.")
            return content
        except FileNotFoundError:
            print(f"The JSON file {json_file_path} does not exist.")
        except json.JSONDecodeError as e:
            print(f"An error occurred while parsing the JSON file {json_file_path}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

# Example of how to use the class (this should be in the comments):
# reader = read_json_file()
# content = reader(json_file_path='/home/heroding/.cache/huggingface/datasets/downloads/bb3eef7d0e0a0283bff6e45060ed0fc57055c2e324d7efc7dc322d5055d1e2da.json')
