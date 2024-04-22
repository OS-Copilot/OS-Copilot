import openai
import logging
import os
import time
import requests
import json


class LLAMA3:
    """
    A class for interacting with the OpenAI API, allowing for chat completion requests.

    This class simplifies the process of sending requests to OpenAI's chat model by providing
    a convenient interface for the chat completion API. It handles setting up the API key
    and organization for the session and provides a method to send chat messages.

    Attributes:
        model_name (str): The name of the model to use for chat completions. Default is set
                          by the global `MODEL_NAME`.
        api_key (str): The API key used for authentication with the OpenAI API. This should
                       be set through the `OPENAI_API_KEY` global variable.
        organization (str): The organization ID for OpenAI. Set this through the
                            `OPENAI_ORGANIZATION` global variable.
    """

    def __init__(self):
        """
        Initializes the OpenAI object with the given configuration.
        """

        self.model_name = 'llama3'

        self.llama_serve = "http://localhost:11434/api/chat"

    def chat(self, messages, temperature=0):
        """
        Sends a chat completion request to the OpenAI API using the specified messages and parameters.

        Args:
            messages (list of dict): A list of message dictionaries, where each dictionary
                                     should contain keys like 'role' and 'content' to
                                     specify the role (e.g., 'system', 'user') and content of
                                     each message.
            temperature (float, optional): Controls randomness in the generation. Lower values
                                           make the model more deterministic. Defaults to 0.

        Returns:
            str: The content of the first message in the response from the OpenAI API.

        """
        payload = {
            "model": "llama3",
            "messages": [
                {
                    "role": "user",
                    "content": "why is the sky blue?"
                }],
            "stream": False
            
        }

        headers = {
                "Content-Type": "application/json"}

        response = requests.post(self.llama_serve, data=json.dumps(payload),headers=headers)

        if response.status_code == 200:
            # Get the response data
            logging.info(f"""Response: {response.json()["message"]["content"]}""")
            return response.json()["message"]["content"]
        else:
            logging.error("Failed to call LLM: ", response.status_code, response.text)
            return ""

llm = LLAMA3()
print(llm.chat(messages=111))