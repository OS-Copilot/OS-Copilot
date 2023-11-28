
from jarvis.action.base_action import BaseAction
import subprocess

class DownloadAndPlayAudio(BaseAction):
    def __init__(self):
        self._description = "Download audio from the given link and play it in the system"

    def __call__(self, link):
        """
        Download audio from the given link and play it in the system.

        Args:
            link (str): The URL of the audio file to be downloaded.

        Returns:
            None
        """
        # Download the audio file to the desktop
        subprocess.run(["wget", link, "-P", "~/Desktop"])

        # Get the file name from the link
        file_name = link.split("/")[-1]

        # Play the audio file
        subprocess.run(["xdg-open", f"~/Desktop/{file_name}"])

# Example usage
task = DownloadAndPlayAudio()
task("https://example.com/audio.mp3")
