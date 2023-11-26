import subprocess

def enable_do_not_disturb():
    # This function uses AppleScript to enable Do Not Disturb mode on a Mac.
    applescript = f"""
    tell application "Shortcuts Events"
        run shortcut "enable_do_not_disturb"
    end tell
    """
    subprocess.run(["osascript", "-e", applescript])

enable_do_not_disturb()