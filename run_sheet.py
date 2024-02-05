import json
import logging
import argparse
from jarvis.agent.jarvis_agent import JarvisAgent
import os

EXCEL_TAKS_PROTMPT = '''
You need to do some tasks related to excel manipulation.
{context} It has a sheet called Sheet1.
Your task is: {task}
The file path of the excel is: {file_path}. You should complete the task and save the result directly in this excel file.
'''

def main():
    parser = argparse.ArgumentParser(description='Inputs')
    parser.add_argument('--action_lib_path', type=str, default='../jarvis/action_lib', help='tool repo path')
    parser.add_argument('--config_path', type=str, default='config.json', help='openAI config file path')
    parser.add_argument('--excel_tasks_path', type=str, default='../tasks/SheetTasks/sheet_task.jsonl', help='excel tasks json path')
    parser.add_argument('--task_id', type=int, default=16, help='excel test set task_id')
    parser.add_argument('--logging_filedir', type=str, default='log/sheet/after', help='excel test set cache dir path')
    args = parser.parse_args()
    logging.basicConfig(filename=os.path.join(args.logging_filedir, "{}.log".format(args.task_id)), level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    jarvis_agent = JarvisAgent(config_path=args.config_path, action_lib_dir=args.action_lib_path)
    planning_agent = jarvis_agent.planner
    retrieve_agent = jarvis_agent.retriever
    execute_agent = jarvis_agent.executor
    task_list = []
    with open(args.excel_tasks_path, 'r') as file:
        for idx,line in enumerate(file):
            task_info = json.loads(line)
            current_task = EXCEL_TAKS_PROTMPT.format(context=task_info["Context"], task=task_info["Instructions"], file_path=task_info["file_path"])
            task_list.append(current_task)

    task = task_list[args.task_id]
    logging.info(task)
   # relevant action 
    retrieve_action_name = retrieve_agent.retrieve_action_name(task)
    retrieve_action_description_pair = retrieve_agent.retrieve_action_description_pair(retrieve_action_name)

    # decompose task
    planning_agent.decompose_task(task, retrieve_action_description_pair)

    # iter each subtask
    while planning_agent.execute_list:
        action = planning_agent.execute_list[0]
        action_node = planning_agent.action_node[action]
        description = action_node.description
        logging.info("The current subtask is: {subtask}".format(subtask=description))
        code = ''
        # The return value of the current task
        result = ''
        next_action = action_node.next_action
        relevant_code = {}
        type = action_node.type
        pre_tasks_info = planning_agent.get_pre_tasks_info(action)
        if type == 'Code':
            # retrieve existing action
            retrieve_name = retrieve_agent.retrieve_action_name(description, 3)
            relevant_code = retrieve_agent.retrieve_action_code_pair(retrieve_name)
        # task execute step
        if type == 'QA':
            # result = execute_agent.question_and_answer_action(pre_tasks_info, task, task)
            if planning_agent.action_num == 1:
                result = execute_agent.question_and_answer_action(pre_tasks_info, task, task)
            else:
                result = execute_agent.question_and_answer_action(pre_tasks_info, task, description)
            print(result)
            logging.info(result)
        else:
            invoke = ''
            if type == 'API':
                api_path = execute_agent.extract_API_Path(description)
                code = execute_agent.api_action(description, api_path, pre_tasks_info)
            else:
                code, invoke = execute_agent.generate_action(action, description, pre_tasks_info, relevant_code)
            # Execute python tool class code
            state = execute_agent.execute_action(code, invoke, type)   
            result = state.result 
            logging.info(state) 
        # Check whether the code runs correctly, if not, amend the code
        if type == 'Code':
            need_mend = False
            trial_times = 0
            critique = ''
            score = 0
            # If no error is reported, check whether the task is completed
            if state.error == None:
                critique, judge, score = execute_agent.judge_action(code, description, state, next_action)
                if not judge:
                    print("critique: {}".format(critique))
                    need_mend = True
            else:
                #  Determine whether it is caused by an error outside the code
                reasoning, error_type = execute_agent.analysis_action(code, description, state)
                if error_type == 'replan':
                    relevant_action_name = retrieve_agent.retrieve_action_name(reasoning)
                    relevant_action_description_pair = retrieve_agent.retrieve_action_description_pair(relevant_action_name)
                    planning_agent.replan_task(reasoning, action, relevant_action_description_pair)
                    continue
                need_mend = True   
            # The code failed to complete its task, fix the code
            while (trial_times < execute_agent.max_iter and need_mend == True):
                trial_times += 1
                print("current amend times: {}".format(trial_times))
                new_code, invoke = execute_agent.amend_action(code, description, state, critique, pre_tasks_info)
                critique = ''
                code = new_code
                # Run the current code and check for errors
                state = execute_agent.execute_action(code, invoke, type)
                result = state.result
                logging.info(state) 
                # print(state)
                # Recheck
                if state.error == None:
                    critique, judge, score = execute_agent.judge_action(code, description, state, next_action)
                    # The task execution is completed and the loop exits
                    if judge:
                        need_mend = False
                        break
                    # print("critique: {}".format(critique))
                else: # The code still needs to be corrected
                    need_mend = True

            # If the task still cannot be completed, an error message will be reported.
            if need_mend == True:
                print("I can't Do this Task!!")
                break
            else: # The task is completed, if code is save the code, args_description, action_description in lib
                if score >= 8:
                    execute_agent.store_action(action, code)
        print("Current task execution completed!!!")  
        planning_agent.update_action(action, result, relevant_code, True, type)
        planning_agent.execute_list.remove(action)
if __name__ == '__main__':
    main()


