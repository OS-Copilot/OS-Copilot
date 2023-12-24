
from jarvis.action.base_action import BaseAction
import os

class search_word(BaseAction):
    def __init__(self):
        self._description = "Search each text file for a specified word and return the paths of files that contain the word."

    def __call__(self, file_paths, search_term, *args, **kwargs):
        """
        Search each text file in the provided list for the specified word and return the paths of files that contain the word.

        Args:
            file_paths (list): List of absolute paths to text files to be searched.
            search_term (str): The word to search for within the text files.

        Returns:
            list: The paths of files that contain the search term.
        """
        matching_files = []
        for file_path in file_paths:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    if search_term in file.read():
                        matching_files.append(file_path)
            except FileNotFoundError:
                print(f"The file {file_path} does not exist.")
            except Exception as e:
                print(f"An error occurred while searching the file {file_path}: {e}")

        print(f"Task execution complete. Found {len(matching_files)} files containing the word '{search_term}'.")
        return matching_files

# Example of how to use the class (this should be in the comments):
# searcher = search_word()
# result = searcher(file_paths=['/path/to/file1.txt', '/path/to/file2.txt'], search_term='agent')
