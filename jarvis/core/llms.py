import os
import openai
import time
import json

proxy = {
'http': '127.0.0.1:2081',
'https': '127.0.0.1:2081',
}


class OpenAI:
    """
    A wrapper for OpenAI API
    """
    def __init__(self, config_path=None):
        with open(config_path) as f:
            config = json.load(f)
        self.model_name = config['model_name']
        openai.api_key = config['OPENAI_API_KEY']
        openai.organization = config['OPENAI_ORGANIZATION']
        openai.proxy = proxy

    def chat(self, messages, temperature=0, sleep_time=2):
        response = openai.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=temperature
        )
        # time.sleep(sleep_time)
        # return response['choices'][0]['message']
        return response.choices[0].message.content


