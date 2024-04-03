import openai
import logging
import os
from dotenv import load_dotenv


load_dotenv(override=True)
MODEL_NAME = os.getenv('MODEL_NAME')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_ORGANIZATION = os.getenv('OPENAI_ORGANIZATION')
BASE_URL = os.getenv('OPENAI_BASE_URL')


class OpenAI:
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

        self.model_name = MODEL_NAME

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
        response = openai.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=temperature
        )
        logging.info(f"Response: {response.choices[0].message.content}")

        return response.choices[0].message.content

def main():
    message = [
            {"role": "user", "content": 'hello'},
        ]
    # print(OPENAI_API_KEY)
    # print(BASE_URL)
    llm = OpenAI()
    print(llm.chat(message))

if __name__ == '__main__':
    main()
