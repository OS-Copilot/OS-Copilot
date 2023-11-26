import subprocess
import datetime

def set_20_minute_alarm():
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

set_20_minute_alarm()
