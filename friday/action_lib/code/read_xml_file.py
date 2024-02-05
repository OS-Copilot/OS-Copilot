
from jarvis.action.base_action import BaseAction
import os
import xml.etree.ElementTree as ET

class read_xml_file(BaseAction):
    def __init__(self):
        self._description = "Read the full text content of the specified XML file."

    def __call__(self, file_path, *args, **kwargs):
        """
        Read the content of the specified XML file and return its content.

        Args:
            file_path (str): The absolute path to the XML file to be read.

        Returns:
            str: The content of the XML file, or None if an error occurs.
        """
        try:
            # Change the current working directory to the directory of the file
            os.chdir(os.path.dirname(file_path))
            
            # Parse the XML file
            tree = ET.parse(os.path.basename(file_path))
            root = tree.getroot()
            
            # Convert the XML tree to a string
            content = ET.tostring(root, encoding='unicode')
            
            print(f"Task execution complete. Content of the XML file {file_path} read successfully.")
            return content
        except FileNotFoundError:
            print(f"The XML file {file_path} does not exist.")
            return None
        except ET.ParseError as e:
            print(f"An error occurred while parsing the XML file {file_path}: {e}")
            return None
        except Exception as e:
            print(f"An error occurred while reading the XML file {file_path}: {e}")
            return None

# Example of how to use the class (this should be in the comments):
# reader = read_xml_file()
# content = reader(file_path='/home/heroding/.cache/huggingface/datasets/downloads/4b570797236b2208d14d90be2da93e5c6ce24b1e73d43d9632136e43effa2ad1.xml')
