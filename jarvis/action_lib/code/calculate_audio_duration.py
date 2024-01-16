from jarvis.action.base_action import BaseAction
from pydub import AudioSegment
import os

class calculate_audio_duration(BaseAction):
    def __init__(self):
        self._description = "Calculate the duration of the specified audio file and return the duration in seconds."

    def __call__(self, audio_file_path, *args, **kwargs):
        """
        Calculate the duration of the specified audio file and return the duration in seconds.

        Args:
            audio_file_path (str): The absolute path to the audio file.

        Returns:
            float: The duration of the audio file in seconds.
        """
        try:
            # Ensure the audio file exists
            if not os.path.isfile(audio_file_path):
                print(f"The audio file {audio_file_path} does not exist.")
                return
            
            # Load the audio file
            audio = AudioSegment.from_file(audio_file_path)
            
            # Calculate the duration in milliseconds and convert to seconds
            duration_seconds = len(audio) / 1000.0
            
            print(f"Task execution complete. Duration of the audio file {audio_file_path} is {duration_seconds} seconds.")
            return duration_seconds
        except FileNotFoundError:
            print(f"The audio file {audio_file_path} does not exist.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

# Example of how to use the class (this should be in the comments):
# duration_calculator = calculate_audio_duration()
# duration = duration_calculator(audio_file_path='/path/to/audio/file.mp3')