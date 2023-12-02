from jarvis.action.base_action import BaseAction
import subprocess

class view_cpu_usage(BaseAction):
    def __init__(self):
        self._description = "Open the terminal interface and view the system's CPU usage."

    def __call__(self, working_directory=None, *args, **kwargs):
        """
        Open the terminal interface and view the system's CPU usage.

        Args:
        working_directory (str): The working directory where the terminal will be opened. If not provided, the current working directory will be used.

        Returns:
        None
        """
        try:
            # Set the working directory
            if working_directory:
                subprocess.run(["gnome-terminal", "--working-directory", working_directory, "--", "top"])
            else:
                subprocess.run(["gnome-terminal", "--", "top"])
        except Exception as e:
            print(f"An error occurred: {e}")
