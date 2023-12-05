from jarvis.action.base_action import BaseAction
# from jarvis.atom_action.operations.system import terminal_show_file_content
# import requests
import subprocess


class enable_do_not_disturb(BaseAction):
    def __init__(self) -> None:
        super().__init__()
        self._description = "enable do not disturb mode"
        self.action_type = 'Python'

    def __call__(self) -> None:
        # This function uses AppleScript to enable Do Not Disturb mode on a Mac.
        applescript = f"""
        tell application "Shortcuts Events"
            run shortcut "enable_do_not_disturb"
        end tell
        """
        subprocess.run(["osascript", "-e", applescript])
