import os
import logging
from oscopilot.prompts.friday_pt import prompt
from oscopilot.utils import self_learning_print_logging, get_project_root_path


class SelfLearning: 
    """
    A class designed to facilitate self-learning for software-related topics by automatically generating and
    engaging with courses based on provided software and package information.
    
    Attributes:
        config (dict): Configuration settings for the learning process.
        agent (object): An external agent or tool that interacts with the learning content or environment.
        learner (object): A learner object that is responsible for designing the course.
        tool_manager (object): Manages the tools required for course creation and learning.
        text_extractor (object, optional): An optional component responsible for extracting text from files.
        course (dict): A dictionary to store course details.
    """

    def __init__(self, agent, learner, tool_manager, config, text_extractor=None):
        """
        Initializes the SelfLearning class with necessary components like agent, learner, tool manager, and configuration.

        Parameters:
            agent (object): The executing agent that will run or simulate the course.
            learner (object): A learning module or tool responsible for course creation.
            tool_manager (object): Manages and orchestrates the use of external tools necessary for course operations.
            config (dict): Configuration parameters that guide the self-learning process.
            text_extractor (callable, optional): A function or callable that extracts text from provided file paths.
        """
        super().__init__()
        self.config = config
        self.agent = agent   
        self.learner = learner(prompt['self_learning_prompt'], tool_manager)      
        self.course = {}
        if text_extractor:
            self.text_extractor = text_extractor(agent)

    def self_learning(self, software_name, package_name, demo_file_path, file_content=None):
        """
        Initiates the self-learning process by designing a course and triggering the learning mechanism.

        Args:
            software_name (str): The name of the software for which the course is being designed.
            package_name (str): The name of the software package related to the course.
            demo_file_path (str): The file path of a demo or example file that is relevant to the course content.
        Returns:
            None.
        """
        self_learning_print_logging(self.config)
        if demo_file_path:
            if not os.path.isabs(demo_file_path):
                demo_file_path = get_project_root_path() + demo_file_path  # TODO: test abs path
            if not file_content:
                file_content = self.text_extract(demo_file_path)
        self.course = self.course_design(software_name, package_name, demo_file_path, file_content)
        self.learn_course(self.course)

    def text_extract(self, demo_file_path):
        """
        Extracts text from the specified demo file path using the configured text extractor.

        Args:
            demo_file_path (str): The path to the demo file from which content needs to be extracted.

        Returns:
            str: The extracted content from the file.
        """
        file_content = self.text_extractor.extract_file_content(demo_file_path)
        return file_content
    
    def course_design(self, software_name, package_name, demo_file_path, file_content=None):
        """
        Designs a course based on the provided software and package name, using content extracted from a demo file.

        Args:
            software_name (str): The name of the software for which the course is designed.
            package_name (str): The package name related to the software.
            demo_file_path (str): Path to the demo file used as content for the course.
            file_content (str, optional): Content of the demo file to be included in the course.

        Returns:
            dict: The designed course as a dictionary.
        """
        course = self.learner.design_course(software_name, package_name, demo_file_path, file_content)
        return course


    def learn_course(self, course):
        """
        Triggers the learning of the designed course using the configured agent.

        Args:
            course (dict): The course dictionary containing lesson details to be learned.
        Returns:
            None.
        """
        logging.info(f'There are {len(self.course)} lessons in the course.')
        for name, lesson in course.items():
            logging.info(f"The current lesson is: {name}")
            logging.info(f"The current lesson content is: {lesson}")
            self.agent.run(lesson)


    def continuous_learning(self, software_name, package_name, demo_file_path=None):
        """
        Implements a continuous learning process that updates and applies new courses based on a designed curriculum.

        Args:
            software_name (str): Name of the software being learned.
            package_name (str): Name of the package within the software.
            demo_file_path (str, optional): Path to a demo file used for extracting text content. Defaults to None.

        Returns:
            None: This method does not return anything but updates internal states and possibly external resources.
        """

        # Initialize variable to hold file content if needed
        file_content = None
        if demo_file_path:
            if not os.path.isabs(demo_file_path):
                demo_file_path = get_project_root_path() + demo_file_path  # TODO: test abs path
                file_content = self.text_extract(demo_file_path)
        self.self_learning(software_name, package_name, demo_file_path, file_content)

        # Continuously design and apply new courses
        while True:
            current_course = str(self.course)
            new_course = self.learner.design_course(software_name, package_name, demo_file_path, file_content, current_course)
            self.course.update(new_course)
            self.learn_course(new_course)



        