import os
import logging
from oscopilot.prompts.friday_pt import prompt
from oscopilot.utils import self_learning_print_logging, get_project_root_path


class SelfLearning:     
    def __init__(self, agent, learner, tool_manager, config, text_extractor=None):
        super().__init__()
        self.config = config
        self.agent = agent   
        self.learner = learner(prompt['self_learning_prompt'], tool_manager)      
        self.course = {}
        if text_extractor:
            self.text_extractor = text_extractor(agent)

    def self_learning(self, software_name, package_name, demo_file_path):
        """
        Start the self learning process.
        """
        self_learning_print_logging(self.config)
        file_content = None
        if demo_file_path:
            if not os.path.isabs(demo_file_path):
                demo_file_path = get_project_root_path() + demo_file_path  # TODO: test abs path
            file_content = self.text_extract(demo_file_path)
        self.course = self.course_design(software_name, package_name, demo_file_path, file_content)
        self.learn_course(self.course)

    def text_extract(self, demo_file_path):
        """
        Extract the content of the file.
        """
        file_content = self.text_extractor.extract_file_content(demo_file_path)
        return file_content
    
    def course_design(self, software_name, package_name, demo_file_path, file_content=None):
        """
        Design the course based on the content of the file.
        """
        course = self.learner.design_course(software_name, package_name, demo_file_path, file_content)
        return course


    def learn_course(self, course):
        """
        Learn the course designed by the learner.
        """
        logging.info(f'There are {len(self.course)} lessons in the course.')
        for name, lesson in course.items():
            logging.info(f"The current lesson is: {name}")
            logging.info(f"The current lesson content is: {lesson}")
            self.agent.run(lesson)


    def continuous_learning(self):
        pass