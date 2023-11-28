from jarvis.action.base_action import BaseAction
from action.get_os_version import get_os_version, check_os_version
from jarvis.atom_action.operations.media import view_office_document

class open_document(BaseAction):
    def __init__(self) -> None:
        super().__init__()
        self._description = "open the target document in your offered file path."
        self.system_version = get_os_version()
        try:
            check_os_version(self.system_version)
        except ValueError as e:
            print(e)
        self.action_type = 'BASH'

    def __call__(self, path: str, *args, **kwargs):
        view_office_document(path, self.system_version)


