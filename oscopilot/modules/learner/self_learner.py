from oscopilot.modules.base_module import BaseModule
from oscopilot.utils.utils import send_chat_prompts


class SelfLearner(BaseModule):
    """
    This class represents a self-learning module that designs educational courses based on given parameters.
    It inherits from BaseModule, utilizing its initialization and utility methods.
    
    Attributes:
        prompt (dict): A dictionary containing system and user prompts for generating course designs.
        tool_manager (object): An instance of a tool manager to handle external tool interactions.
        course (dict): A dictionary to store course details that are generated based on user and system inputs.
    """
    def __init__(self, prompt, tool_manager):
        """
        Initializes the SelfLearner class with the necessary prompts and tool manager.
        
        Args:
            prompt (dict): Contains the necessary prompts for generating the course design.
            tool_manager (object): Manages interactions with external tools needed for course design.
        """
        super().__init__()
        self.prompt = prompt
        self.tool_manager = tool_manager
        self.course = {}
        
    def design_course(self, software_name, package_name, demo_file_path, file_content=None, prior_course=None):
        """
        Designs a course based on specified software and content parameters and stores it in the course attribute.
        
        Args:
            software_name (str): The name of the software around which the course is centered.
            package_name (str): The name of the software package relevant to the course.
            demo_file_path (str): Path to the demo file that will be used in the course.
            file_content (str): The content of the file that will be demonstrated or used in the course.
            prior_course (str): The course that has been completed.
        
        Returns:
            dict: A dictionary containing the designed course details.
        
        Uses system and user prompts to create a conversation with a language model or similar system, to generate
        a course based around the provided parameters. The response is then parsed into JSON format and saved.
        """
        sys_prompt = self.prompt['_SYSTEM_COURSE_DESIGN_PROMPT']
        user_prompt = self.prompt['_USER_COURSE_DESIGN_PROMPT'].format(
            system_version = self.system_version,
            software_name = software_name,
            package_name = package_name,
            file_content = file_content,
            demo_file_path = demo_file_path,
            prior_course = prior_course
        )
        response = send_chat_prompts(sys_prompt, user_prompt, self.llm)
        # logging.info(f"The overall response is: {response}")
        course = self.extract_json_from_string(response)
        self.course = course
        return self.course