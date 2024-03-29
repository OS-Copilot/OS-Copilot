from typing import Optional


class BaseAction:
    """
    A base class for defining actions with optional attributes like description, name, 
    timeout, and action type.

    This class serves as a template for defining various actions that can be executed
    within a system. It encapsulates common properties that any action would require,
    such as a name, description, execution timeout, and the type of action. The class
    is designed to be extended by more specific action implementations.

    Attributes:
        _name (str): The name of the action. Defaults to the class name if not provided.
        _description (Optional[str]): A brief description of what the action does.
        _timeout (int): The maximum time in seconds the action is allowed to run. Defaults to 2.
        action_type (str): The type of action, must be one of 'BASH', 'CODE', 'TOOL'. Defaults to 'BASH'.

    Raises:
        AssertionError: If the provided `action_type` is not among the expected types.
        NotImplementedError: If the `__call__` method is not implemented by a subclass.

    Methods:
        __call__(*args, **kwargs): Abstract method, intended to be implemented by subclasses
                                   to execute the action.
        _python(*lines): Constructs a Python command string from the given lines of code.
        _import(*packages): Generates an import statement for importing everything from the
                            specified jarvis package.
        __str__(): Returns the same string representation as `__repr__`.

    Note:
        This class is abstract and is meant to be subclassed to provide concrete implementations
        of actions. The `__call__` method must be overridden by subclasses to define the action's
        behavior when invoked.
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
        """
        The maximum time in seconds the action is allowed to run.

        This read-only property returns the action's execution timeout value. It defines
        how long an action can take before it should be considered as failed or timed out.

        Returns:
            int: The timeout for the action in seconds.
        """
        return self._timeout

    @property
    def name(self):
        """
        The name of the action.

        This read-only property returns the name of the action. If not explicitly set
        during initialization, it defaults to the name of the subclass implementing
        the action.

        Returns:
            str: The name of the action.
        """
        return self._name

    @property
    def description(self):
        """
        A brief description of what the action does.

        This read-only property provides a short description of the action's purpose or
        functionality. It can be used to give users or developers a quick overview of
        what the action is intended to perform.

        Returns:
            Optional[str]: The description of the action, or None if not set.
        """
        return self._description

    def __repr__(self):
        return f'{self.name}:{self.description}'

    def __str__(self):
        return self.__repr__()

if __name__ == '__main__':
    action = BaseAction()