from oscopilot.modules.base_module import BaseModule
from oscopilot.utils.utils import send_chat_prompts


class SelfLearner(BaseModule):
    def __init__(self, prompt, tool_manager):
        super().__init__()
        self.prompt = prompt
        self.tool_manager = tool_manager
        self.course = {}
        
    def design_course(self, software_name, package_name, demo_file_path, file_content):
        sys_prompt = self.prompt['_SYSTEM_COURSE_DESIGN_PROMPT']
        user_prompt = self.prompt['_USER_COURSE_DESIGN_PROMPT'].format(
            system_version = self.system_version,
            software_name = software_name,
            package_name = package_name,
            file_content = file_content,
            demo_file_path = demo_file_path
        )
        response = send_chat_prompts(sys_prompt, user_prompt, self.llm)
        # logging.info(f"The overall response is: {response}")
        course = self.extract_json_from_string(response)
        self.course = course
        return self.course
    