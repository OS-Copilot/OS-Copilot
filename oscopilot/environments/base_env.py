import os
from oscopilot.utils.config import Config
from typing import Optional, Union, List
from oscopilot.utils.schema import EnvState


class BaseEnv:
    """
    A base class for environments configurations in action-based systems.

    This class provides foundational attributes and methods for managing environments,
    including timeouts, working directories, and environmental states. It is designed
    to be extended by subclasses that implement specific environments behaviors.
    """

    def __init__(self) -> None:
        """
        Initializes the environments with default settings.

        Sets up the working directory, applying a default timeout and preparing the
        environments state. If the working directory does not exist, it is created.
        """
        self._name: str = self.__class__.__name__
        self.timeout: int = 300
        working_dir = Config.get_parameter('working_dir')
        if os.path.isabs(working_dir):
            self.working_dir = working_dir
        else:
            self.working_dir = os.path.abspath(os.path.join(__file__, "..", "..", "..", working_dir))
        if not os.path.exists(self.working_dir):
            os.makedirs(self.working_dir)

        self.env_state: Union[EnvState, None] = None

    def step(self, code):
        """
        Generator that yields a dictionary in LMC format:
        {"type": "console", "format": "output", "content": "a printed statement"}
        {"type": "console", "format": "active_line", "content": "1"}
        {"type": "image", "format": "base64", "content": "{base64}"}
        """
        return {"type": "console", "format": "output", "content": code}

    def stop(self):
        """
        Halts code execution, but does not terminate state.
        """
        pass

    def terminate(self):
        """
        Terminates state.
        """
        pass

    def list_working_dir(self):
        """
        Lists the contents of the working directory in a detailed format.

        Returns a string representation similar to the output of the 'ls' command in Linux,
        including file/directory names, sizes, and types.

        Returns:
            str: Detailed listings of the working directory's contents, or an error message if the directory does not exist.
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
                doc_type = 'Directory'
            else:
                doc_type = 'File'

            details.append(f"{name}\t {size} bytes\t {doc_type}")

        return "\n".join(details)
        
    def step(self, _command) -> EnvState:
        """
        Executes a command within the environments.

        This method is intended to be implemented by subclasses, defining how commands
        are processed and their effects on the environments state.

        Args:
            _command: The command to be executed.

        Raises:
            NotImplementedError: Indicates that the subclass must implement this method.

        Returns:
            EnvState: The state of the environments after executing the command.
        """
        raise NotImplementedError

    def reset(self):
        """
        Resets the environments to its initial state.

        This method is intended to be implemented by subclasses, defining the specific
        actions required to reset the environments.
        """
        working_dir = Config.get_parameter('working_dir')
        if os.path.isabs(working_dir):
            self.working_dir = working_dir
        else:
            self.working_dir = os.path.abspath(os.path.join(__file__, "..", "..", "..", working_dir))
    
    @property
    def name(self):
        """
        The name of the environments.

        Returns:
            str: The name of the environments, typically set to the class name unless overridden in a subclass.
        """
        return self._name

    def __repr__(self):
        """
        Provides a string representation of the environments.

        Returns:
            str: A representation of the environments, including its name.
        """
        return f'{self.name}'

    def __str__(self):
        """
        Returns the string representation of the environments, mirroring `__repr__`.

        Returns:
            str: A string representation of the environments.
        """
        return self.__repr__()


if __name__ == '__main__':
    env = BaseEnv()
    env.env_state = EnvState()
    # result = env.observe()
