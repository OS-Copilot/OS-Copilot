from openai import OpenAI

class Audio2TextTool:
    def __init__(self) -> None:
        self.client = OpenAI()
    def caption(self,audio_file):
        # Perform voice recognition using the OpenAI Whisper API
        response = self.client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
        return response.texts