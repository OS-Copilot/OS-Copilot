import openai
import json
import logging

class OpenAI:
    """
      OPEN AI Chat Models
    """
    def __init__(self, config_path=None):
        with open(config_path) as f:
            config = json.load(f)
        self.model_name = config['model_name']
        openai.api_key = config['OPENAI_API_KEY']
        openai.organization = config['OPENAI_ORGANIZATION']
        print(openai.api_key)
        print(openai.organization)
        # openai.proxy = proxy

    def chat(self, messages, temperature=0, sleep_time=2):
        response = openai.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=temperature
        )
        logging.info(response.choices[0].message.content)

        # time.sleep(sleep_time)
        # return response['choices'][0]['message']
        return response.choices[0].message.content


