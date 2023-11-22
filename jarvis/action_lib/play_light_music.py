import subprocess

def play_light_music():
    # Plays a playlist named "light music" in iTunes or Music app
    applescript = """
    tell application "Music"
        play playlist "light music"
    end tell
    """
    subprocess.run(["osascript", "-e", applescript])

play_light_music()