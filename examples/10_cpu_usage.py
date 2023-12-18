from jarvis.agent.openai_agent import OpenAIAgent
from jarvis.environment.py_env import PythonEnv
from jarvis.agent.linux_skill_create_agent import LinuxSkillCreateAgent
import time
'''
Made By DZC & WZM
target: View system CPU usage.
'''
# environment
environment = PythonEnv()
# path of action lib
action_lib_path = "../jarvis/action_lib"
# use to look up existed skill code and extract information
retrieve_agent = OpenAIAgent(config_path="./config.json")
# use to create new skills
skill_create_agent = LinuxSkillCreateAgent(config_path="./config.json")

# We assume that the response result comes from the task planning agent.
response = '''
Thought: In order to solve this task, we need to open the terminal interface in the current operating system environment and call relevant instructions on this terminal to view the system's CPU usage.

Actions: 
1. <action>view_cpu_usage</action> <description>open the terminal interface in the current operating system environment and call relevant instructions on the terminal to view the system's CPU usage.</description>
Check local action_lib, the required action code is in the library, according to the function description in the code, combined with the information provided by the user, You can instantiate classes for different tasks.

'''

# Get actions and corresponding descriptions
actions = retrieve_agent.extract_information(response, begin_str='<action>', end_str='</action>')
task_descriptions = retrieve_agent.extract_information(response, begin_str='<description>', end_str='</description>')

# Loop all the actions
for action, description in zip(actions, task_descriptions):
    # Create python tool class code
    create_msg = skill_create_agent.skill_create_format_message(task_name=action, task_description=description, working_dir=environment.working_dir)
    code = skill_create_agent.extract_python_code(create_msg)
    print(code)

    # Create the invoke of the tool class
    invoke_msg = skill_create_agent.invoke_generate_format_message(code, description,working_dir=environment.working_dir)
    invoke = skill_create_agent.extract_information(invoke_msg,  begin_str='<invoke>', end_str='</invoke>')[0]
    print("************************<invoke>**************************")
    print(invoke)
    print("************************</invoke>*************************")
    code = code + '\n' + invoke

    # Run the tool code
    state = environment.step(code)
    print(state)

    # Check whether the code runs correctly, if not, amend the code
    need_mend = False
    trial_times = 0
    critique = ''
    # If no error is reported, check whether the task is completed
    if state.error == None:
        judge_result = skill_create_agent.task_judge_format_message(code, description, state.result, state.pwd, state.ls)
        critique = judge_result['reasoning']
        judge = judge_result['judge']
        if judge == False:
            print("critique: {}".format(critique))
            need_mend = True
    else:
        need_mend = True    
    # The code failed to complete its task, fix the code
    current_code = code
    while (trial_times < 3 and need_mend == True):
        trial_times += 1
        print("current amend times: {}".format(trial_times))
        amend_msg = skill_create_agent.skill_amend_format_message(current_code, description, state.error, state.result, state.pwd, state.ls, critique)
        print(amend_msg)
        new_code = skill_create_agent.extract_python_code(amend_msg)
        current_code = new_code
        # Run the current code and check for errors
        state = environment.step(current_code)
        print(state)
        # Recheck
        if state.error == None:
            judge_result = skill_create_agent.task_judge_format_message(current_code, description, state.result, state.pwd, state.ls)
            critique = judge_result['reasoning']
            judge = judge_result['judge']
            # The task execution is completed and the loop exits
            if judge == True:
                need_mend = False
                break
            print("critique: {}".format(critique))
        else: # The code still needs to be corrected
            need_mend = True

    # If the task still cannot be completed, an error message will be reported.
    if need_mend == True:
        print("I can't Do this Task!!")
    else: # The task is completed, save the code in lib
        file_path = action_lib_path + "/" + action + '.py'
        with open(file_path, 'w', encoding='utf-8') as f:
            lines = current_code.strip().splitlines()
            if lines:
                # Remove the invoke code of the python file
                lines.pop()
            final_code = '\n'.join(lines)
            f.write(final_code)


