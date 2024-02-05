from openai import OpenAI
import os

os.environ["OPENAI_API_KEY"] = "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"
os.environ["OPENAI_ORGANIZATION"] = "org-fSyygvftM73W0pK4VjoK395W"

class Audio2TextTool:
    def __init__(self) -> None:
        self.client = OpenAI()
    def caption(self,audio_file):
        # 使用 OpenAI Whisper API 进行语音识别
        response = self.client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
        return response.texts