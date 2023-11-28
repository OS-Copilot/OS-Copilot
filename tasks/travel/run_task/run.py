import copy
import json
import os
import re
import time

import openai
import requests

from jarvis.agent.react_agent import ReactAgent
from jarvis.agent.openai_agent import OpenAIAgent
from simulator import TravelSimulator
# from utils.code import get_content, get_content_list
# from utils.config_manager import ConfigManager
# from utils.travel import execute_sql,execute_python
from general import ConfigManager


TASK = '''Bob is in Beijing and going to travel in several cities, please make a ticket purchase plan and travel sequence for him.The demands are as follows:
1. visit ['Chengdu']. The order doesn't matter and he needs to return to Beijing finally.
2. He is free to travel from 2023.7.1 to 2023.7.20. The budget for transportation is 1800.0 CNY.
3. Play at least 1 day in Chengdu.
4. Stay in any city for a minimum of 24 hours to count as one day.
5. On the basis of completing the above conditions (especially the budget), spend as little time as possible.
'''

# os.environ['OPENAI_API_KEY'] = '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'
os.environ['OPENAI_API_KEY'] = 'hk-y7oqw81000007081956c9eae69ef0ec39fb67374833ee3f4'
# model_name = 'gpt-3.5-turbo-16k-0613'
model_name = 'gpt-4-1106-preview'
MAX_ITER = 3
level = 1
begin = 24
end = 99
step = 1



def get_content(s, begin_str='[BEGIN]', end_str='[END]'):
    _begin = s.find(begin_str)
    _end = s.find(end_str)
    if _begin == -1 or _end == -1:
        return ''
    else:
        return s[_begin + len(begin_str):_end].strip()


def get_content_list(s, begin_str='[BEGIN]', end_str='[END]'):
    result = []
    _begin = s.find(begin_str)
    if _begin>=0:
        _end = s[_begin + len(begin_str):].find(end_str) + _begin + len(begin_str)
    else:
        _end = s.find(end_str)
    while not (_begin == -1 or _end == -1):
        result.append(s[_begin + len(begin_str):_end].strip())
        s = s[_end + len(end_str):]
        _begin = s.find(begin_str)
        _end = s.find(end_str)
    unique_result = []
    for item in result:
        if item not in unique_result:
            unique_result.append(item)
    return unique_result


def query_database(query: list):
    # config_manager.clear_proxies()
    try:
        response = requests.post(
            "http://localhost:8079/tools/database",
            json={'queries': query}
        )
        response = response.json()
        if len(response) > 0:
            response = response[0]
    except Exception as e:
        response = {'result': f'error', 'error': f'run error{e}'}
        print(response)
    # config_manager.apply_proxies()
    return re.sub(r'\\n', '\n', str(response))
    # return str(response)


def execute_sql(statement: str):
    return query_database([statement])


def execute_python(code: str):
    config_manager.clear_proxies()
    response = requests.post(
        'http://127.0.0.1:8079/tools/python',
        json={'code': code}
    )
    config_manager.apply_proxies()
    result=response.json()
    return str(result)


def invoke_function(func_data):
    func = globals()[func_data['function_name']]
    result = func(*func_data['args'])
    return result


def run_item(task, agent, output_path="."):
    plan_strs = []
    max_iter = MAX_ITER
    if level == 1:
        from jarvis.core.prompt import TRAVEL_EXAMPLE_MESSAGES_1
        main_agent = ReactAgent(model_name=model_name, task=task,
                               record_path=f'{output_path}/react_agent_record.json',
                               example_message=TRAVEL_EXAMPLE_MESSAGES_1)
    elif level == 2:
        from jarvis.core.prompt import TRAVEL_EXAMPLE_MESSAGES_2
        main_agent = ReactAgent(model_name=model_name, task=task,
                               record_path=f'{output_path}/react_agent_record.json',
                               example_message=TRAVEL_EXAMPLE_MESSAGES_2)
    elif level == 3:
        from jarvis.core.prompt import TRAVEL_EXAMPLE_MESSAGES_3
        main_agent = ReactAgent(model_name=model_name, task=task,
                               record_path=f'{output_path}/react_agent_record.json',
                               example_message=TRAVEL_EXAMPLE_MESSAGES_3)

    cur_iter = 0
    completed = False
    try:
        if 'gpt-4' in model_name:
            session = requests.Session()
        else:
            session = None
        while cur_iter < max_iter:
            call_over = False
            cur_iter += 1
            response = main_agent.get_response(session)
            text = response['content']
            functions = main_agent.parse_functions(text)
            observation = f'No valid action found.\nAvailable actions:{main_agent.get_action_space()}\nGive me the action between <action> and </action>.'
            for function in functions:
                try:
                    if function['function_name'] == 'over':
                        call_over = True
                    observation = invoke_function(function)
                    break
                except Exception as e:
                    observation = f'{e}. No valid action found. Available actions:{main_agent.get_action_space()}\n Give me the action between <action> and </action>. Make sure to pass in the correct parameters'
                    print(e)

            if call_over:
                completed = True
                main_agent.add_over_prompt()
                response = main_agent.get_response(session)
                text = response['content']
                plan_strs = get_content_list(text, begin_str='<plan>', end_str='</plan>')
                break
            print(f'observation={observation}')
            main_agent.add_user_prompt(observation)
        if cur_iter >= max_iter:
            main_agent.add_over_prompt()
            response = main_agent.get_response(session)
            text = response['content']
            plan_strs = get_content(text, begin_str='<plan>', end_str='</plan>')
    # except openai.error.InvalidRequestError as e:
    except openai.BadRequestError as e:
        print(f'{e} InvalidRequestError. Context length error?')
        for idx in range(len(main_agent.messages) - 1, 0, -1):
            if main_agent.messages[idx]["role"] == "user":
                break
        main_agent.messages = main_agent.messages[:idx - 2]  # 从后往前删掉idx:user, idx-1:assistant, idx-2:user
        main_agent.add_over_prompt()
        response = main_agent.get_response(session)
        text = response['content']
        plan_strs = get_content_list(text, begin_str='<plan>', end_str='</plan>')
    finally:
        if session is not None:
            session.close()
    # except Exception as e:
    #     print(f'{e} InvalidRequestError. Context length error?')
    #     for idx in range(len(main_agent.messages) - 1, 0, -1):
    #         if main_agent.messages[idx]["role"] == "user":
    #             break
    #     main_agent.messages = main_agent.messages[:idx - 2]  # 从后往前删掉idx:user, idx-1:assistant, idx-2:user
    #     main_agent.add_over_prompt()
    #     response = main_agent.get_response()
    #     text = response['content']
    #     plan_strs = get_content_list(text, begin_str='<plan>', end_str='</plan>')

    return plan_strs, completed


def run(level, agent):
    output_dir = f'./output/travel/react_style/{agent.llm.model_name}/level{level}'
    data_path = f'./tasks/travel/data/data_level1.json'
    with open(data_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    data = data[begin:end:step]
    for data_idx, d in enumerate(data):
        print(f'data_idx={data_idx}')
        prediction = []
        # try:
        print(f'{data_idx}:{time.localtime()}')
        task_id = begin + data_idx * step
        output_path = f'{output_dir}/{task_id}'
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        prediction_file = f'{output_path}/prediction.json'
        task = d['question']
        simulator = TravelSimulator(**d['demands']['TravelSimulator'])
        simulator.create_constraints(d['demands']['Constraints'])
        plan_strs, completed = run_item(task=task, agent=agent, output_path=output_path)
        for plan_str in plan_strs:
            print(f'plan_str={plan_str}')
            simulator.action(plan_str)
        simulator.over()
        print(f'geterror')
        errors = simulator.get_errors()
        score = simulator.get_score()
        print(f'state={simulator.state}')
        prediction.append(
            {"question": d['question'], "plan": plan_strs, "errors": errors, "score": score,
             "over": completed, "state": str(simulator.state)})
        print(f'prediction={prediction}')
        with open(prediction_file, 'w', encoding='utf-8') as f:
            json.dump(prediction, f, indent=4, ensure_ascii=False)
        # except Exception as e:
        #     print(f'{data_idx}:{e}')


config_manager = ConfigManager()
agent = OpenAIAgent(config_path="examples/config.json")
for level in [1,2,3]:
    run(level, agent)
