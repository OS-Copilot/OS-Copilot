import os
import argparse
import logging
from datasets import load_dataset
from jarvis.agent.jarvis_agent import JarvisAgent


task1 = "Please help me find the GitHub blog of Zhiyong Wu from Shanghai AI Lab. Give me the markdown of the page link, and save the standard Markdown format as wuzhiyong.md in the working directory."
task2 = "Please help me search the github blog homepage of zhiyong Wu who is from hku and summary the content to the wuzhiyong.txt file. In addition, you also need to download a photo of Zhiyong Wu from hku from the Internet to wuzhiyong.jpg."


class GAIALoader:
    def __init__(self, cache_dir=None):
        if cache_dir != None:
            assert os.path.exists(cache_dir), f"Cache directory {cache_dir} does not exist."
            self.cache_dir = cache_dir
            try:
                self.dataset = load_dataset("gaia-benchmark/GAIA", "2023_level1", cache_dir=self.cache_dir)
            except Exception as e:
                raise Exception(f"Failed to load GAIA dataset: {e}")
        else:
            self.dataset = load_dataset("gaia-benchmark/GAIA", "2023_level1")
            
        
    def get_data_by_task_id(self, task_id):
        if self.dataset is None or 'validation' not in self.dataset:
            raise ValueError("Dataset not loaded or validation set not available.")

        validation_set = self.dataset['validation']
        for record in validation_set:
            if record['task_id'] == task_id:
                return record
        return None

def main():
    parser = argparse.ArgumentParser(description='Inputs')
    parser.add_argument('--action_lib_path', type=str, default='../jarvis/action_lib', help='tool repo path')
    parser.add_argument('--config_path', type=str, default='config.json', help='openAI config file path')
    parser.add_argument('--query', type=str, default=task2, help='user query')
    parser.add_argument('--query_file_path', type=str, default='', help='user query file path')
    parser.add_argument('--task_id', type=str, default=None, help='GAIA dataset task_id')
    parser.add_argument('--cache_dir', type=str, default=None, help='GAIA dataset cache dir path')
    parser.add_argument('--logging_filedir', type=str, default='log', help='GAIA dataset cache dir path')
    args = parser.parse_args()

    task_id = args.task_id
    query = args.query
    
    logging.basicConfig(filename=os.path.join(args.logging_filedir, "{}.log".format(task_id)), level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    jarvis_agent = JarvisAgent(config_path=args.config_path, action_lib_dir=args.action_lib_path)
    planning_agent = jarvis_agent.planner
    retrieve_agent = jarvis_agent.retriever
    execute_agent = jarvis_agent.executor

    if task_id:
        print('Use the task_id {} to get the corresponding question in the GAIA dataset.'.format(task_id))
        data = GAIALoader(args.cache_dir).get_data_by_task_id(task_id)
        task = 'Your task is: {0}\nThe path of the files you need to use(if exists): {1}'.format(data['Question'], data['file_path'])
    elif task_id == None and query != '':
        task = 'Your task is: {0}\nThe path of the files you need to use(if exists): {1}'.format(args.query, args.query_file_path)
    else:
        raise ValueError("Task_id and query cannot be both None or both not None.")
    print('Task:\n'+task)


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
            result = execute_agent.question_and_answer_action(pre_tasks_info, task)
            print(result)
        elif type == 'API':
            api_path = execute_agent.extract_API_Path(description)
            code = execute_agent.api_action(description, api_path, pre_tasks_info)
            invoke = ''
        else:
            code, invoke = execute_agent.generate_action(action, description, pre_tasks_info, relevant_code)
        # Execute python tool class code
        state = execute_agent.execute_action(code, invoke, type)   
        result = state.result 
        logging.info(state.result) 
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
                logging.info(result) 
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

