from __future__ import annotations
import subprocess
from oscopilot.utils.schema import EnvState
from oscopilot.environments.env import Env
from tempfile import NamedTemporaryFile


class PythonEnv(Env):
    """
    A base class representing a Python execution environments for actions.

    This class provides a structured way to execute Python code snippets within a
    specified environments, handling the execution state and any outputs or errors
    generated during the execution. It extends the `Env` class, adding Python-specific
    execution capabilities.
    """

    def __init__(self) -> None:
        """
        Initializes the Python environments with default values.
        """
        super().__init__()
        self._name: str = self.__class__.__name__

    def step(self, _command: str, args: list[str] | str = []) -> EnvState:
        """
        Executes a Python command in the environments and updates the environments state.

        This method takes a Python command as input, executes it within the environments's
        working directory, and captures the command's output, error, and final working directory.
        It supports passing arguments to the command and handles execution errors gracefully.

        Args:
            _command (str): The Python command to execute.
            args (list[str] | str, optional): Additional arguments for the command. Can be a list
                of arguments or a space-separated string. Defaults to an empty list.

        Returns:
            EnvState: An object representing the state of the environments after command execution, including any results, errors, and the current working directory.

        Note:
            The method ensures the last line of the output is always the current working directory
            to maintain accurate state tracking.
        """
        tmp_code_file = NamedTemporaryFile("w", dir=self.working_dir, suffix=".py", encoding="utf-8")
        # Solving the issue of not being able to retrieve the current working directory of the last line of output
        _command = _command.strip() + "\n"  + "import os" + "\n" + "print(os.getcwd())"
        tmp_code_file.write(_command)
        tmp_code_file.flush()
        filename = tmp_code_file.name
        if isinstance(args, str):
            args = args.split()  # Convert space-separated string to a list
        self.env_state = EnvState(command=_command)
        try:
            results = subprocess.run(
                ["python", '-B', str(filename)],
                encoding="utf8",
                check=True, cwd=self.working_dir, timeout=self.timeout,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            # If there is standard output.
            if results.stdout:
                stout = results.stdout.strip().split('\n')
                self.env_state.result = "\n".join(stout[:-1])
                self.observe(stout[-1])
                return self.env_state
        except subprocess.CalledProcessError as e:
            self.env_state.error = e.stderr
        except Exception as e:
            self.env_state.error = repr(e)
        finally:
            tmp_code_file.close()
        self.observe(self.working_dir)

        return self.env_state

    def observe(self, pwd):
        """
        Updates the environments state based on the current working directory.

        This method sets the environments's working directory and lists its contents,
        updating the `EnvState` object to reflect the current state of the environments.

        Args:
            pwd (str): The path to set as the current working directory.
        """
        self.env_state.pwd = pwd
        self.working_dir = pwd
        self.env_state.ls = subprocess.run(['ls'], cwd=self.working_dir, capture_output=True, text=True).stdout


DEFAULT_DESCRIPTION = """def solution():
    print("hello world!")
    print("hello world!")
    return "return!"
"""
if __name__ == '__main__':
    env = PythonEnv()
    print(env.step(DEFAULT_DESCRIPTION))
    # print(env.step("cd ../../"))
    # print(env.step("gogo"))
    # env.reset()
    # print(env.step("sleep 3"))
