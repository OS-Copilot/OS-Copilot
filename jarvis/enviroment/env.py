import subprocess
import time
import os
from typing import Optional, Union, List
from jarvis.core.schema import ActionReturn, ActionStatusCode, EnvState


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
        self.timeout: int = 2
        self.working_dir = os.path.abspath(os.path.join(__file__, "..", "..", "..", "working_dir"))
        self.env_state: EnvState | None = None

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
    result = env.observe()
