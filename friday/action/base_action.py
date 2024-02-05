from typing import Optional


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
                 timeout: int = 2,
                 action_type: Optional[str] = 'BASH') -> None:
        if name is None:
            name = self.__class__.__name__
        self._name = name
        self._description = description
        self._timeout = timeout
        assert action_type in ['BASH', 'CODE', 'TOOL']
        self.action_type = action_type

    def __call__(self, *args, **kwargs):
        raise NotImplementedError

    def _python(self, *lines):
        return f'python -Bc "{"; ".join(lines)}"'

    def _import(self, *packages):
        return f'from jarvis.{".".join(packages)} import *'

    @property
    def timeout(self):
        return self._timeout

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