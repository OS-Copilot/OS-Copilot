import os
from jarvis.action.base_action import BaseAction
import subprocess

class view_cpu_usage(BaseAction):
    def __init__(self):
        self._description = "Open the terminal interface and view the system's CPU usage."

    def __call__(self, working_directory=None, *args, **kwargs):
        """
        Open the terminal interface and view the system's CPU usage.

        Args:
        working_directory (str): The working directory where the terminal will be opened.
        
        Returns:
        None
        """
        # Check if working_directory is provided, if not, use the current working directory
        if working_directory:
            # Change the current working directory to the provided working_directory
            os.chdir(working_directory)
        
        # Open the terminal and call relevant instructions to view the system's CPU usage
        subprocess.run(["gnome-terminal", "--", "top"])
