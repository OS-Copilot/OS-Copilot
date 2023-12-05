from jarvis.action.base_action import BaseAction
# from jarvis.atom_action.operations.system import terminal_show_file_content
# import requests
import subprocess


class play_light_music(BaseAction):
    def __init__(self) -> None:
        super().__init__()
        self._description = "play light music"
        self.action_type = 'Python'

    def __call__(self) -> None:
        # This function uses AppleScript to enable Do Not Disturb mode on a Mac.
        applescript = """
        tell application "Music"
            play playlist "light music"
        end tell
        """
        subprocess.run(["osascript", "-e", applescript])


# def play_light_music():
#     # Plays a playlist named "light music" in iTunes or Music app
#     applescript = """
#     tell application "Music"
#         play playlist "light music"
#     end tell
#     """
#     subprocess.run(["osascript", "-e", applescript])

# play_light_music()