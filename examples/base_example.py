from jarvis.agent.openai_agent import OpenAIAgent
from jarvis.agent.jarvis_agent import JarvisAgent

'''
Made By DZC & WZM
target: Classify files in a specified folder.
'''

# path of action lib
action_lib_path = "../jarvis/action_lib"
# args_description_path = action_lib_path + "/args_description"
# action_description_path = action_lib_path + "/action_description"
# code_path = action_lib_path + "/code"
# vectordb_path = action_lib_path + "/vectordb"

# use to look up existed skill code and extract information
retrieve_agent = OpenAIAgent(config_path="./config.json", action_lib_dir=action_lib_path)
# use to create new skills
jarvis_agent = JarvisAgent(config_path="./config.json", action_lib_dir=action_lib_path)
execute_agent = jarvis_agent.executor

# We assume that the response result comes from the task planning agent.
response = '''
Thought: XXX
Actions: 
1. <action>XXX</action> <description>XXX</description>
2. <action>XXX</action> <description>XXX</description>
Check local action_lib, the required action code is in the library, according to the function description in the code, combined with the information provided by the user, You can instantiate classes for different tasks.

'''

# Get actions and corresponding descriptions
actions = retrieve_agent.extract_information(response, begin_str='<action>', end_str='</action>')
task_descriptions = retrieve_agent.extract_information(response, begin_str='<description>', end_str='</description>')

# Loop all the actions
for action, description in zip(actions, task_descriptions):
    # Create python tool class code
    code = execute_agent.generate_action(action, description)
    # Execute python tool class code
    state = execute_agent.execute_action(code, description)
    # Check whether the code runs correctly, if not, amend the code
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
        need_mend = True    
    # The code failed to complete its task, fix the code
    current_code = code
    while (trial_times < execute_agent.max_iter and need_mend == True):
        trial_times += 1
        print("current amend times: {}".format(trial_times))
        new_code = execute_agent.amend_action(current_code, description, state, critique)
        critique = ''
        current_code = new_code
        # Run the current code and check for errors
        state = execute_agent.execute_action(current_code, description)
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
    else: # The task is completed, if code is save the code, args_description, action_description in lib
        if score >= 8:
            execute_agent.store_action(action, current_code)

