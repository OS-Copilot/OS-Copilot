import subprocess
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
        self.timeout = timeout
        # self.function = ''
        # self.imports = []

    # def from_config(self, path):
    #     with open(path, 'r') as file:
    #         lines = file.readlines()
    #         for line in lines:
    #             if line.startswith('import'):
    #                 self.imports.append(line)
    #             else:
    #                 self.function += line
    #     exec(self.function, globals())

    # def __call__(self, *args, **kwargs) -> ActionReturn:
    #     raise NotImplementedError

    def _command(self):
        raise NotImplementedError

    def _success(self):
        raise NotImplementedError

    def __repr__(self):
        return f'{self.name}:{self.description}'

    def __str__(self):
        return self.__repr__()

    def run(self, *args, **kwargs) -> ActionReturn:
        command = self._command()
        action_return = ActionReturn(type=self.name, args=command)
        try:
            result = subprocess.run([command], capture_output=True, check=True,
                                    text=True, shell=True, timeout=self.timeout, stdin=subprocess.DEVNULL)
            if result.returncode == 0:
                action_return.state = ActionStatusCode.SUCCESS
                action_return.thought = self._success()
                if result.stdout:
                    action_return.result = result.stdout
                if result.stderr:
                    action_return.result = result.stderr
        except subprocess.CalledProcessError as e:
            action_return.state = ActionStatusCode.FAILED
            action_return.errmsg = e.stderr
            action_return.result = e.stdout

        return action_return

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description
