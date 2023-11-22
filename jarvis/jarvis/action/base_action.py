import subprocess
import time
import os
from typing import Optional
from jarvis.core.schema import ActionReturn, ActionStatusCode


class BaseAction:
    """Base class for all actions.

    Args:
        description (str, optional): The description of the action. Defaults to
            None.
        name (str, optional): The name of the action. If None, the name will
            be class name. Defaults to None.
    """

    def __init__(self,
                 description: Optional[str] = None,
                 name: Optional[str] = None,
                 timeout: Optional[int] = 2) -> None:
        if name is None:
            name = self.__class__.__name__
        self._name = name
        self._description = description
        self._timeout = timeout
        # self.execute_log_path = execute_log_path
        # self.state_log_path = state_log_path
        # self.log_execute = logging_command + self.execute_log_path
        # self.log_state = logging_command + self.state_log_path
        # self.working_dir = os.path.abspath(os.path.join(os.getcwd(), "..", "..", "working_dir"))
        # self.server_name = "test"
        # print(self.working_dir)

    def _python(self, *lines):
        return f'python -Bc "{"; ".join(lines)}"'

    def _import(self, *packages):
        return f'from jarvis.{".".join(packages)} import *'

    @property
    def _command(self):
        raise NotImplementedError

    @property
    def timeout(self):
        return self._timeout
    # def _success(self):
    #     raise NotImplementedError
    # def execute_command(self, command):
    #     subprocess.run(["tmux", "send-keys", "-t", self.server_name, command, "Enter"])

    # async def parse_result(self):

    # def __call__(self, *args, **kwargs) -> ActionReturn:

    # def run(self, *args, **kwargs) -> ActionReturn:
    #     # 将run搬到env中？
    #     command = self._command() + self.log_execute
    #     subprocess.run(["tmux", "send-keys", "-t", self.server_name, command, "Enter"])
    #     time.sleep(self.timeout)
        # with open()
        # action_return = ActionReturn(type=self.name, args=command)
        # try:
            # result = subprocess.run([command], capture_output=True, check=True,
            #                         text=True, shell=True, timeout=self.timeout, stdin=subprocess.DEVNULL)
        # result = subprocess.run(["tmux", "send-keys", "-t", 'test', command, "Enter"])
        #     if result.returncode == 0:
        #         action_return.state = ActionStatusCode.SUCCESS
        #         action_return.thought = self._success()
        #         if result.stdout:
        #             action_return.result = result.stdout
        #         if result.stderr:
        #             action_return.result = result.stderr
        # except subprocess.CalledProcessError as e:
        #     action_return.state = ActionStatusCode.FAILED
        #     action_return.errmsg = e.stderr
        #     action_return.result = e.stdout

        # return action_return

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    def __repr__(self):
        return f'{self.name}:{self.description}'

    def __str__(self):
        return self.__repr__()

if __name__ == '__main__':
    action = BaseAction()