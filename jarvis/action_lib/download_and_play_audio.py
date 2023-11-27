# from jarvis.action.base_action import BaseAction
# import subprocess
# import requests
# import os

# class download_and_play_audio(BaseAction):
#     def __init__(self):
#         self._description = "This class downloads an audio file from a provided URL and plays it on a Linux desktop."

#     def __call__(self, url, *args, **kwargs):
#         """
#         Downloads an audio file from the specified URL and plays it.

#         Args:
#             url (str): URL of the audio file to be downloaded.
#             *args, **kwargs: Additional arguments and keyword arguments.

#         Usage:
#             download_and_play_audio = Download_And_Play_Audio()
#             download_and_play_audio('http://example.com/audio.mp3')
#         """
#         # Download the audio file
#         try:
#             response = requests.get(url)
#             response.raise_for_status()
#             file_name = self._format_file_name(url)
#             desktop_path = os.path.join(os.path.expanduser('~'), '桌面', file_name)
#             with open(desktop_path, 'wb') as file:
#                 file.write(response.content)
#         except Exception as e:
#             print(f"Error downloading file: {e}")
#             return

#         # Play the audio file
#         try:
#             subprocess.run(['xdg-open', desktop_path], check=True)
#         except subprocess.CalledProcessError as e:
#             print(f"Error playing file: {e}")

#     def _format_file_name(self, url):
#         """
#         Formats the file name from the URL to prevent garbled characters.

#         Args:
#             url (str): The URL of the file.

#         Returns:
#             str: Formatted file name.
#         """
#         return url.split('/')[-1].replace(' ', '_')
import subprocess
import os
from jarvis.action.base_action import BaseAction

class download_and_play_audio(BaseAction):
    def __init__(self):
        self._description = "Download audio from a given link and play it on the system."

    def __call__(self, link):
        """
        Download audio from a given link and play it on the system.

        Args:
            link (str): The URL of the audio file to download.

        Returns:
            str: A message indicating whether the operation was successful or not.
        """
        try:
            # Define the desktop folder name based on the system language
            desktop_folder = "桌面"  # Chinese system language
            # Expand the '~' character to the user's home directory
            desktop_path = os.path.expanduser(f"~/{desktop_folder}/audio_file.mp3")
            # Use the subprocess library to download the audio file to the desktop
            subprocess.run(["wget", link, "-O", desktop_path])
            # Use a media player to play the downloaded audio file
            subprocess.run(["xdg-open", desktop_path])
            return "Audio downloaded and playing."
        except Exception as e:
            return f"Error: {str(e)}"

# Example usage of the class
if __name__ == "__main__":
    downloader = download_and_play_audio()
    result = downloader("https://dasex101-random-learning.oss-cn-shanghai.aliyuncs.com/DataEthics/Taylor%20Swift%20-%20Look%20What%20You%20Made%20Me%20Do.mp3")

    print(result)

