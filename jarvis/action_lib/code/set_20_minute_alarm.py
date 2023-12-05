from jarvis.action.base_action import BaseAction
# from jarvis.atom_action.operations.system import terminal_show_file_content
# import requests
import subprocess
import datetime


class set_20_minute_alarm(BaseAction):
    def __init__(self) -> None:
        super().__init__()
        self._description = "set 20 minute alarm"
        self.action_type = 'Python'

    def __call__(self) -> None:
        # Sets an alarm for 20 minutes from now using AppleScript
        # The script creates a new reminder with an alert
        current_time = datetime.datetime.now()
        alarm_time = current_time + datetime.timedelta(minutes=20)
        alarm_time_str = alarm_time.strftime('%Y-%m-%d %H:%M:%S')

        applescript = f"""
        tell application "Reminders"
            set newReminder to make new reminder
            tell newReminder
                set name to "20 Minute Alarm"
                set remind me date to date "{alarm_time_str}"
            end tell
        end tell
        """
        subprocess.run(["osascript", "-e", applescript])

# def set_20_minute_alarm():
#     # Sets an alarm for 20 minutes from now using AppleScript
#     # The script creates a new reminder with an alert
#     current_time = datetime.datetime.now()
#     alarm_time = current_time + datetime.timedelta(minutes=20)
#     alarm_time_str = alarm_time.strftime('%Y-%m-%d %H:%M:%S')

#     applescript = f"""
#     tell application "Reminders"
#         set newReminder to make new reminder
#         tell newReminder
#             set name to "20 Minute Alarm"
#             set remind me date to date "{alarm_time_str}"
#         end tell
#     end tell
#     """
#     subprocess.run(["osascript", "-e", applescript])

# set_20_minute_alarm()
