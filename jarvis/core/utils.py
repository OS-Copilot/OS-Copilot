import copy
import numpy as np
import itertools
import json
import logging
import os
import re
import string
from typing import Any
import tqdm
import re
import tiktoken

def num_tokens_from_string(string: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model('gpt-4-1106-preview')
    num_tokens = len(encoding.encode(string))
    return num_tokens



def parse_content(content, type="html.parser"):
    implemented = ["html.parser", "lxml", "lxml-xml", "xml", "html5lib"]
    if type not in implemented:
        raise ValueError(f"Parser type {type} not implemented. Please choose one of {implemented}")

    from bs4 import BeautifulSoup

    soup = BeautifulSoup(content, type)
    original_size = len(str(soup.get_text()))

    tags_to_exclude = [
        "nav",
        "aside",
        "form",
        "header",
        "noscript",
        "svg",
        "canvas",
        "footer",
        "script",
        "style",
    ]
    for tag in soup(tags_to_exclude):
        tag.decompose()

    ids_to_exclude = ["sidebar", "main-navigation", "menu-main-menu"]
    for id in ids_to_exclude:
        tags = soup.find_all(id=id)
        for tag in tags:
            tag.decompose()

    classes_to_exclude = [
        "elementor-location-header",
        "navbar-header",
        "nav",
        "header-sidebar-wrapper",
        "blog-sidebar-wrapper",
        "related-posts",
    ]
    for class_name in classes_to_exclude:
        tags = soup.find_all(class_=class_name)
        for tag in tags:
            tag.decompose()

    content = soup.get_text()
    content = clean_string(content)

    cleaned_size = len(content)
    if original_size != 0:
        logging.info(
            f"Cleaned page size: {cleaned_size} characters, down from {original_size} (shrunk: {original_size-cleaned_size} chars, {round((1-(cleaned_size/original_size)) * 100, 2)}%)"  # noqa:E501
        )

    return content


def clean_string(text):
    """
    This function takes in a string and performs a series of text cleaning operations.

    Args:
        text (str): The text to be cleaned. This is expected to be a string.

    Returns:
        cleaned_text (str): The cleaned text after all the cleaning operations
        have been performed.
    """
    # Replacement of newline characters:
    text = text.replace("\n", " ")

    # Stripping and reducing multiple spaces to single:
    cleaned_text = re.sub(r"\s+", " ", text.strip())

    # Removing backslashes:
    cleaned_text = cleaned_text.replace("\\", "")

    # Replacing hash characters:
    cleaned_text = cleaned_text.replace("#", " ")

    # Eliminating consecutive non-alphanumeric characters:
    # This regex identifies consecutive non-alphanumeric characters (i.e., not
    # a word character [a-zA-Z0-9_] and not a whitespace) in the string
    # and replaces each group of such characters with a single occurrence of
    # that character.
    # For example, "!!! hello !!!" would become "! hello !".
    cleaned_text = re.sub(r"([^\w\s])\1*", r"\1", cleaned_text)

    return cleaned_text


def is_readable(s):
    """
    Heuristic to determine if a string is "readable" (mostly contains printable characters and forms meaningful words)

    :param s: string
    :return: True if the string is more than 95% printable.
    """
    try:
        printable_ratio = sum(c in string.printable for c in s) / len(s)
    except ZeroDivisionError:
        logging.warning("Empty string processed as unreadable")
        printable_ratio = 0
    return printable_ratio > 0.95  # 95% of characters are printable





def format_source(source: str, limit: int = 20) -> str:
    """
    Format a string to only take the first x and last x letters.
    This makes it easier to display a URL, keeping familiarity while ensuring a consistent length.
    If the string is too short, it is not sliced.
    """
    if len(source) > 2 * limit:
        return source[:limit] + "..." + source[-limit:]
    return source




# check if the source is valid json string
def is_valid_json_string(source: str):
    try:
        _ = json.loads(source)
        return True
    except json.JSONDecodeError:
        logging.error(
            "Insert valid string format of JSON. \
            Check the docs to see the supported formats - `https://docs.embedchain.ai/data-sources/json`"
        )
        return False




def chunks(iterable, batch_size=100, desc="Processing chunks"):
    """A helper function to break an iterable into chunks of size batch_size."""
    it = iter(iterable)
    total_size = len(iterable)

    with tqdm(total=total_size, desc=desc, unit="batch") as pbar:
        chunk = tuple(itertools.islice(it, batch_size))
        while chunk:
            yield chunk
            pbar.update(len(chunk))
            chunk = tuple(itertools.islice(it, batch_size))

def generate_prompt(template: str, replace_dict: dict):
    prompt = copy.deepcopy(template)
    for k, v in replace_dict.items():
        prompt = prompt.replace(k, str(v))
    return prompt

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))\
    

def get_open_api_description_pair(json_path="openapi.json"):
    with open(json_path, 'r') as file:
        open_api_json = json.load(file)
    open_api_dict = open_api_json['paths']
    open_api_description_pair = {}
    for name, value in open_api_dict.items():
        if 'post' in value:
            open_api_description_pair[name] = value['post']['summary']
        else:
            open_api_description_pair[name] = value['get']['summary']
    return open_api_description_pair

print(get_open_api_description_pair())
    
# prompt =  '''
#         You are an expert in making plans. 
#         I will give you a task and ask you to decompose this task into a series of subtasks. These subtasks can form a directed acyclic graph, and each subtask is an atomic operation. Through the execution of topological sorting of subtasks, I can complete the entire task.
#         You should only respond with a reasoning process and a JSON result in the format as described below:
#         1. Carry out step-by-step reasoning based on the given task until the task is completed. Each step of reasoning is decomposed into sub-tasks. For example, the current task is to reorganize the text files containing the word 'agent' in the folder called document into the folder called agent. Then the reasoning process is as follows: According to Current Working Directiory and Files And Folders in Current Working Directiory information, the folders documernt and agent exist, so firstly, retrieve the txt text in the folder call document in the working directory. If the text contains the word "agent", save the path of the text file into the list, and return. Secondly, put the retrieved files into a folder named agent based on the file path list obtained by executing the previous task.
#         2. Each decomposed subtask has three attributes: name, task description, and dependencies. The 'name' abstracts an appropriate name based on the reasoning process of the current subtask, and 'description' is the process of the current subtask. 'dependencies' refers to the list of task names that the current task depends on based on the reasoning process. These tasks must be executed before the current task.
#         3. In JSON, each decomposed subtask contains three attributes: name, description, and dependencies, which are obtained through reasoning about the task. The key of each subtask is the name of the subtask.
#         4. Continuing with the example in 1, the format of the JSON data I want to get is as follows:
#         {
#             'retrieve_files' : {
#                 'name': 'retrieve_files',
#                 'description': 'retrieve the txt text in the folder call document in the working directory. If the text contains the word "agent", save the path of the text file into the list, and return.',
#                 'dependencies': []
#             },
#             'organize_files' : {
#                 'name': 'organize_files',
#                 'description': 'put the retrieved files into a folder named agent based on the file path list obtained by executing the previous task.',
#                 'dependencies': ['retrieve_files']
#             }    
#         }        
#         And you should also follow the following criteria:
#         1. A task can be decomposed down into one or more atomic operations, depending on the complexity of the task.
#         2. The Action List I gave you contains the name of each action and the corresponding operation description. These actions are all atomic operations. You can refer to these atomic operations to decompose the current task.
#         3. If an atomic action in the Action List can be used to process the currently decomposed sub-task, then the name of the decomposed sub-task should be directly adopted from the name of that atomic action.
#         4. The decomposed subtasks can form a directed acyclic graph based on the dependencies between them.
#         5. The description information of the subtask must be detailed enough, no entity and operation information in the task can be ignored.
#         6. 'Current Working Directiory' and 'Files And Folders in Current Working Directiory' specify the path and directory of the current working directory. These information may help you understand and generate tasks.
#         7. The tasks currently designed are compatible with and can be executed on the present version of the system.
#         8. The current task may need the return results of its predecessor tasks. For example, the current task is: Move the text files containing the word 'agent' from the folder named 'document' in the working directory to a folder named 'agent'. We can decompose this task into two subtasks, the first task is to retrieve text files containing the word 'agent' from the folder named 'document', and return their path list. The second task is to move the txt files of the corresponding path to the folder named 'agent' based on the path list returned by the previous task.
#         9. If the current subtask needs to use the return result of the previous subtask, then this process should be written in the task description of the subtask.
#         10. Please note that the name of a subtask must be abstract. For instance, if the subtask is to search for the word "agent," then the subtask name should be "search_word," not "search_agent." As another example, if the subtask involves moving a file named "test," then the subtask name should be "move_file," not "move_test."
#         11. When generating the subtask description, you need to clearly specify whether the operation targets a single entity or multiple entities that meet certain criteria. 
#         12. When decomposing subtasks, avoid including redundant information. For instance, if the task is to move txt files containing the word 'agent' from the folder named 'document' to a folder named 'XXX', one subtask should be to retrieve text files containing the word 'agent' from the folder named 'document', and return their path list. Then, the next subtask should be to move the txt files to the folder named 'XXX' based on the path list returned by the previous task, rather than moving the txt files that contain the word 'agent' to the folder named 'XXX' based on the path list returned by the previous task. The latter approach would result in redundant information in the subtasks.
#         '''
# print(num_tokens_from_string(prompt))


# {
#      "paths": {
#     "/tools/python": {
#       "post": {
#         "summary": "Execute Python",
#         "operationId": "execute_python_tools_python_post",
#         "requestBody": {
#           "content": {
#             "application/json": {
#               "schema": {
#                 "$ref": "#/components/schemas/Item"
#               }
#             }
#           },
#           "required": true
#         },
#         "responses": {
#           "200": {
#             "description": "Successful Response",
#             "content": {
#               "application/json": {
#                 "schema": {}
#               }
#             }
#           },
#           "422": {
#             "description": "Validation Error",
#             "content": {
#               "application/json": {
#                 "schema": {
#                   "$ref": "#/components/schemas/HTTPValidationError"
#                 }
#               }
#             }
#           }
#         }
#       }
#     }
#   }
# }