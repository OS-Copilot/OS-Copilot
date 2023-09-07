import os
import requests


from utils.template import PromptTemplate
from utils.api_service import chat_gpt
from utils.file import *
from utils.config_manager import ConfigManager
config_manager = ConfigManager()


def query_database(query: list):
    config_manager.clear_proxies()
    try:
        response = requests.post(
            "http://localhost:8079/tools/database",
            json={'queries': query}
        )
        response = response.json()
    except Exception as e:
        response = f'run error{e}'
        print(response)
    config_manager.apply_proxies()
    return response[0]['result']


def action(action_str):
    try:
        print(f'action={action_str}')
        result = eval(action_str)
        return result
    except Exception as e:
        return f"An error occurred: {e}"


def execute_sql(statement: str):
    return query_database([statement])
