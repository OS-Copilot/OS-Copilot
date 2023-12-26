from jarvis.agent.jarvis_agent import JarvisAgent

'''
Made By DZC
'''

# path of action lib
action_lib_path = "../jarvis/action_lib"
jarvis_agent = JarvisAgent(config_path="./config.json", action_lib_dir=action_lib_path)
planning_agent = jarvis_agent.planner
retrieve_agent = jarvis_agent.retriever
execute_agent = jarvis_agent.executor

# task = '''
# Move the text files containing the word 'agent' from the folder named 'document' to the path '/home/heroding/桌面/Jarvis/working_dir/agent'.
# '''

task = '''
给我下载一张华东师范大学的照片。
'''

# relevant action 
retrieve_action_name = retrieve_agent.retrieve_action_name(task)
retrieve_action_description_pair = retrieve_agent.retrieve_action_description_pair(retrieve_action_name)
# decompose task
planning_agent.decompose_task(task, retrieve_action_description_pair)

# retrieve existing action
for action_name, action_node in planning_agent.action_node.items():
    type = action_node.type
    if type == 'General':
        action_description = action_node.description
        retrieve_action = retrieve_agent.retrieve_action_name(action_description, 3)
        retrieve_action_code_pair = retrieve_agent.retrieve_action_code_pair(retrieve_action)
        planning_agent.update_action(action_name, relevant_action=retrieve_action_code_pair)

# iter each subtask
while planning_agent.execute_list:
    action = planning_agent.execute_list[0]
    action_node = planning_agent.action_node[action]
    description = action_node.description
    code = action_node.code
    relevant_code = action_node.relevant_action
    type = action_node.type
    pre_tasks_info = planning_agent.get_pre_tasks_info(action)
    if type == 'QA':
        answer = execute_agent.question_and_answer_action(pre_tasks_info, task)
        print(answer)
        break
    # Create python tool class code and invoke
    if type == 'API':
        api_path = execute_agent.extract_API_Path(description)
        code = execute_agent.api_action(description, api_path, pre_tasks_info)
        invoke = ''
    else:
        code, invoke = execute_agent.generate_action(action, description, pre_tasks_info, relevant_code)
    # Execute python tool class code
    state = execute_agent.execute_action(code, invoke, type)
    current_code = ''
    # Check whether the code runs correctly, if not, amend the code
    if type == 'General':
        need_mend = False
        trial_times = 0
        critique = ''
        score = 0
        # If no error is reported, check whether the task is completed
        if state.error == None:
            critique, judge, score = execute_agent.judge_action(code, description, state)
            if not judge:
                print("critique: {}".format(critique))
                need_mend = True
        else:
            #  Determine whether it is caused by an error outside the code
            reasoning, error_type = execute_agent.analysis_action(code, description, state)
            if error_type == 'replan':
                relevant_action_name = retrieve_agent.retrieve_action_name(reasoning)
                relevant_action_description_pair = retrieve_agent.retrieve_action_description_pair(relevant_action_name)
                planning_agent.replan_task(reasoning, action)
                continue
            need_mend = True   
        # The code failed to complete its task, fix the code
        current_code = code
        while (trial_times < execute_agent.max_iter and need_mend == True):
            trial_times += 1
            print("current amend times: {}".format(trial_times))
            new_code, invoke = execute_agent.amend_action(current_code, description, state, critique, pre_tasks_info)
            critique = ''
            current_code = new_code
            # Run the current code and check for errors
            state = execute_agent.execute_action(current_code, invoke, type)
            # print(state)
            # Recheck
            if state.error == None:
                critique, judge, score = execute_agent.judge_action(current_code, description, state)
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
            if score >= 7:
                execute_agent.store_action(action, current_code)
    print("Current task execution completed!!!")
    planning_agent.update_action(action, current_code, state.result, status=True, type=type)
    planning_agent.execute_list.remove(action)

