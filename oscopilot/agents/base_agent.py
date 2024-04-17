import re
import json
from oscopilot.utils import get_os_version


class BaseAgent:
    """
    BaseAgent serves as the foundational class for all agents types within the system.

    This class initializes the core attributes common across different agents, providing
    a unified interface for further specialization. Attributes include a language learning
    model, the execution environments, an action library, and a maximum iteration limit for
    agents operations.

    Attributes:
        llm: Placeholder for a language learning model, initialized as None.
        environments: The execution environments for the agents, initialized as None.
        action_lib: A library of actions available to the agents, initialized as None.
        max_iter: The maximum number of iterations the agents can perform, initialized as None.
    """
    def __init__(self):
        """
        Initializes a new instance of BaseAgent with default values for its attributes.
        """
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
            result.append(message[_begin + len(begin_str):_end])
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