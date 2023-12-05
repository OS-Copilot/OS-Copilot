from jarvis.action.base_action import BaseAction


class organize_app_layout(BaseAction):
    def __init__(self) -> None:
        super().__init__()
        self._description = "Using organize_app_layout() will help user reorganize their Desktop layout for better working condition and focus more easily."
        self._timeout = 15

    def __call__(self, *args, **kwargs):
        return 'shortcuts run "Organize APP Layout"'

    # @property
    # def _command(self) -> str:
    #     return 'shortcuts run "Organize APP Layout"'
    #
    # def _success(self) -> str:
    #     return "Successfully organized the app's layout"
