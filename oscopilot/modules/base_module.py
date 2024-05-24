import re
import json
import os
from oscopilot.utils.llms import OpenAI, OLLAMA
# from oscopilot.environments.py_env import PythonEnv
# from oscopilot.environments.py_jupyter_env import PythonJupyterEnv
from oscopilot.environments import Env
from oscopilot.utils import get_os_version
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env', override=True)
MODEL_TYPE = os.getenv('MODEL_TYPE')

class BaseModule:
    def __init__(self):
        """
        Initializes a new instance of BaseModule with default values for its attributes.
        """
        if MODEL_TYPE == "OpenAI":
            self.llm = OpenAI()
        elif MODEL_TYPE == "OLLAMA":
            self.llm = OLLAMA()
        # self.environment = PythonEnv()
        # self.environment = PythonJupyterEnv()
        self.environment = Env()
        self.system_version = get_os_version()
        
    def extract_information(self, message, begin_str='[BEGIN]', end_str='[END]'):
        """
        Extracts substrings from a message that are enclosed within specified begin and end markers.

        Args:
            message (str): The message from which information is to be extracted.
            begin_str (str): The marker indicating the start of the information to be extracted.
            end_str (str): The marker indicating the end of the information to be extracted.

        Returns:
            list[str]: A list of extracted substrings found between the begin and end markers.
        """
        result = []
        _begin = message.find(begin_str)
        _end = message.find(end_str)
        while not (_begin == -1 or _end == -1):
            result.append(message[_begin + len(begin_str):_end].lstrip("\n"))
            message = message[_end + len(end_str):]
            _begin = message.find(begin_str)
            _end = message.find(end_str)
        return result  

    def extract_json_from_string(self, text):
        """
        Identifies and extracts JSON data embedded within a given string.

        This method searches for JSON data within a string, specifically looking for
        JSON blocks that are marked with ```json``` notation. It attempts to parse
        and return the first JSON object found.

        Args:
            text (str): The text containing the JSON data to be extracted.

        Returns:
            dict: The parsed JSON data as a dictionary if successful.
            str: An error message indicating a parsing error or that no JSON data was found.
        """
        # Improved regular expression to find JSON data within a string
        json_regex = r'```json\s*\n\{[\s\S]*?\n\}\s*```'
        
        # Search for JSON data in the text
        matches = re.findall(json_regex, text)

        # Extract and parse the JSON data if found
        if matches:
            # Removing the ```json and ``` from the match to parse it as JSON
            json_data = matches[0].replace('```json', '').replace('```', '').strip()
            try:
                # Parse the JSON data
                parsed_json = json.loads(json_data)
                return parsed_json
            except json.JSONDecodeError as e:
                return f"Error parsing JSON data: {e}"
        else:
            return "No JSON data found in the string."
        

    def extract_list_from_string(self, text):
        """
        Extracts a list of task descriptions from a given string containing enumerated tasks.
        This function ensures that only text immediately following a numbered bullet is captured,
        and it stops at the first newline character or at the next number, preventing the inclusion of subsequent non-numbered lines or empty lines.

        Parameters:
        text (str): A string containing multiple enumerated tasks. Each task is numbered and followed by its description.

        Returns:
        list[str]: A list of strings, each representing the description of a task extracted from the input string.
        """

        # Regular expression pattern:
        # \d+\. matches one or more digits followed by a dot, indicating the task number.
        # \s+ matches one or more whitespace characters after the dot.
        # ([^\n]*?) captures any sequence of characters except newlines (non-greedy) as the task description.
        # (?=\n\d+\.|\n\Z|\n\n) is a positive lookahead that matches a position followed by either a newline with digits and a dot (indicating the start of the next task),
        # or the end of the string, or two consecutive newlines (indicating a break between tasks or end of content).
        task_pattern = r'\d+\.\s+([^\n]*?)(?=\n\d+\.|\n\Z|\n\n)'

        # Use the re.findall function to search for all matches of the pattern in the input text.
        data_list = re.findall(task_pattern, text)

        # Return the list of matched task descriptions.
        return data_list