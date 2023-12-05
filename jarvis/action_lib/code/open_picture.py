from jarvis.action.base_action import BaseAction


class open_picture(BaseAction):
    def __init__(self) -> None:
        super().__init__()
        self._description = "Using open_picture() will open the picture you want."
        self.action_type = 'BASH'

    def __call__(self, *args, **kwargs):
        return 'shortcuts run "open_picture"'
