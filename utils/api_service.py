import json
import requests
import os
import openai
import time
import numpy as np


def chat_gpt(messages, model_name="gpt-3.5-turbo", sleep_time=2, temperature=0, functions=None):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if functions is None:
        response = openai.ChatCompletion.create(
            model=model_name,
            messages=messages,
            temperature=temperature
        )
    else:
        response = openai.ChatCompletion.create(
            model=model_name,
            messages=messages,
            temperature=temperature,
            functions=functions
        )
    time.sleep(sleep_time)
    return response['choices'][0]['message']


def get_init_chat():
    return [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

