from friday.action.base_action import BaseAction
import re
import json


class BaseAgent:
    """
    BaseAgent is the base class of all agents.
    """
    def __init__(self):
        self.llm = None
        self.environment = None
        self.action_lib = None
        self.max_iter = None
        # self.action_lib_description = {}
        # self.action = None
        # self.retrieval_top_k = None
        # self.action_lib_dir = None
        # self.init_action_lib()
        
    # Extract information from text
    def extract_information(self, message, begin_str='[BEGIN]', end_str='[END]'):
        result = []
        _begin = message.find(begin_str)
        _end = message.find(end_str)
        while not (_begin == -1 or _end == -1):
            result.append(message[_begin + len(begin_str):_end])
            message = message[_end + len(end_str):]
            _begin = message.find(begin_str)
            _end = message.find(end_str)
        return result  

    # egular expression to find JSON data within a string
    def extract_json_from_string(self, text):
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