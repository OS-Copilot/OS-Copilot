import os

from typing import Optional, Union, List
from friday.core.schema import EnvState


class Env:
    """Base class for all actions.

    Args:
        description (str, optional): The description of the action. Defaults to
            None.
        name (str, optional): The name of the action. If None, the name will
            be class name. Defaults to None.
    """

    def __init__(self) -> None:
        self._name: str = self.__class__.__name__
        self.timeout: int = 300
        self.working_dir = os.path.abspath(os.path.join(__file__, "..", "..", "..", "working_dir"))
        if not os.path.exists(self.working_dir):
            os.makedirs(self.working_dir)

        self.env_state: Union[EnvState, None] = None

    def list_working_dir(self):
        """
        Lists files and directories in the given directory with details similar to 'ls' command in Linux.
        """
        directory = self.working_dir
        # Check if the directory exists
        if not os.path.exists(directory):
            return f"Directory '{directory}' does not exist."

        # List files and directories
        files_and_dirs = os.listdir(directory)

        # Create a list to store the details
        details = []

        for name in files_and_dirs:
            # Get the full path
            full_path = os.path.join(directory, name)

            # Get file or directory size
            size = os.path.getsize(full_path)

            # Check if it's a file or directory
            if os.path.isdir(full_path):
                type = 'Directory'
            else:
                type = 'File'

            details.append(f"{name}\t {size} bytes\t {type}")

        return "\n".join(details)
        


    def step(self, _command) -> EnvState:
        raise NotImplementedError

    def reset(self):
        raise NotImplementedError
    @property
    def name(self):
        return self._name

    def __repr__(self):
        return f'{self.name}'

    def __str__(self):
        return self.__repr__()


if __name__ == '__main__':
    env = Env()
    env.env_state = EnvState()
    # result = env.observe()
