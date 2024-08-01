import os
import argparse
import logging
from oscopilot.utils.utils import random_string, get_project_root_path
import dotenv
import sys

dotenv.load_dotenv(dotenv_path='.env', override=True)


class Config:
    """
    A singleton class for storing and accessing configuration parameters.

    This class ensures that only one instance is created and provides methods for initializing and accessing parameters.
    """    
    _instance = None

    @classmethod
    def initialize(cls, args):
        """
        Initializes the Config instance with command-line arguments.

        Args:
            args (argparse.Namespace): The parsed command-line arguments.
        """        
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            cls._instance.parameters = vars(args)

    @classmethod
    def get_parameter(cls, key):
        """
        Retrieves a parameter value by key.

        Args:
            key (str): The key of the parameter to retrieve.

        Returns:
            Any: The value of the parameter if found, otherwise None.
        """        
        if cls._instance is None:
            return None
        return cls._instance.parameters.get(key, None)


def setup_config():
    """
    Sets up configuration parameters based on command-line arguments.

    Returns:
        argparse.Namespace: The parsed command-line arguments.
    """
    # Create an argument parser
    parser = argparse.ArgumentParser(description='Inputs')

    parser.add_argument('--generated_tool_repo_path', type=str, default='oscopilot/tool_repository/generated_tools', help='generated tool repo path')
    parser.add_argument('--working_dir', type=str, default='working_dir', help='working dir path')
    parser.add_argument('--query', type=str, default=None, help='Enter your task')
    parser.add_argument('--query_file_path', type=str, default='', help='Enter the path of the files for your task or leave empty if not applicable')
    parser.add_argument('--max_repair_iterations', type=int, default=3, help='Sets the max number of repair attempts. Default is 3.')
    parser.add_argument('--logging_filedir', type=str, default='log', help='log path')
    parser.add_argument('--logging_filename', type=str, default='temp0325.log', help='log file name')
    parser.add_argument('--logging_prefix', type=str, default=random_string(16), help='log file prefix')
    parser.add_argument('--score', type=int, default=8, help='critic score > score => store the tool')


    # for Self-Leanring
    parser.add_argument('--software_name', type=str, default='Excel', help='The name of the software used for learning.')
    parser.add_argument('--package_name', type=str, default='openpyxl', help='The name of the package used for learning.')
    parser.add_argument('--demo_file_path', type=str, default=get_project_root_path() + 'working_dir/Invoices.xlsx', help='Entering the path of the demo file helps you design the course, or leave it empty if not applicable.')


    # for GAIA
    parser.add_argument('--dataset_cache', type=str, default=None, help='Path to the dataset cache folder')
    parser.add_argument('--level', type=int, default=1, help='Specifies the level of the GAIA dataset to use. Valid options are 1, 2, or 3')
    parser.add_argument('--dataset_type', type=str, default='test', help='Defines the type of dataset to use, either `validation` for development or `test` for testing purposes')
    parser.add_argument('--gaia_task_id', type=str, default=None, help='GAIA dataset task_id')


    # for SheetCopilot
    parser.add_argument('--sheet_task_id', type=int, default=1, help='sheet task dataset task id')

    # Check if the script is being run in a test environment
    if 'pytest' in sys.modules:
        # In a test environment, use default values
        args = parser.parse_args([])
    else:
        # In a non-test environment, parse command-line arguments
        args = parser.parse_args()


    Config.initialize(args)

    if not os.path.exists(args.logging_filedir):
        os.mkdir(args.logging_filedir)

    logging.basicConfig(
        filename=os.path.join(args.logging_filedir, args.logging_filename),
        level=logging.INFO,
        format=f'[{args.logging_prefix}] %(asctime)s - %(levelname)s - %(message)s'
    )

    return args


def setup_pre_run(args):
    """
    Sets up pre-run tasks and logging.

    Args:
        args (argparse.Namespace): The parsed command-line arguments.

    Returns:
        str: A string containing information about the task.
    """    
    task = 'Your task is: {0}'.format(args.query)
    if args.query_file_path != '':
        task = task + '\nThe path of the files you need to use: {0}'.format(args.query_file_path)

    print('Task:\n'+task)
    logging.info(task)
    return task


def self_learning_print_logging(args):
    """
    Prints self-learning task information and logs it.

    Args:
        args (argparse.Namespace): The parsed command-line arguments.
    """
    task = 'Your task is: Learn to use {0} to operate {1}'.format(args.package_name, args.software_name)
    if args.demo_file_path != '':
        task = task + '\nThe path of the file helps you design the course: {0}'.format(args.demo_file_path)

    print('Task:\n'+task)
    logging.info(task)