from oscopilot.prompts.friday_pt import prompt


class TextExtractor:
    def __init__(self, agent):
        super().__init__()
        self.agent = agent
        self.prompt = prompt['text_extract_prompt']
    
    def extract_file_content(self, file_path):
        """
        Extract the content of the file.
        """
        extract_task = self.prompt.format(file_path=file_path)
        self.agent.run(extract_task)
        file_content = list(self.agent.planner.tool_node.values())[-1].return_val
        return file_content