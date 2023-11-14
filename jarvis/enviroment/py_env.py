import subprocess
import time
import os
from typing import Optional, Union, List
from jarvis.core.schema import ActionReturn, ActionStatusCode, EnvState
from jarvis.enviroment.env import Env
from tempfile import NamedTemporaryFile


class PythonEnv(Env):
    """Base class for all actions.

    Args:
        description (str, optional): The description of the action. Defaults to
            None.
        name (str, optional): The name of the action. If None, the name will
            be class name. Defaults to None.
    """

    def __init__(self) -> None:
        super().__init__()
        self._name: str = self.__class__.__name__

    def step(self, _command: str, args: list[str] | str = []) -> EnvState:

        tmp_code_file = NamedTemporaryFile("w", dir=self.working_dir, suffix=".py", encoding="utf-8")
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
                stdout=subprocess.PIPE
            )
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

    def reset(self):
        self.working_dir = os.path.abspath(os.path.join(__file__, "..", "..", "..", "working_dir"))

    def observe(self, pwd):
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
