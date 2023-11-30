from jarvis.agent.openai_agent import OpenAIAgent
from jarvis.enviroment.py_env import PythonEnv
from jarvis.agent.linux_skill_creator import LinuxSkillCreator
from jarvis.agent.linux_skill_amend import LinuxSkillAmend
from jarvis.agent.linux_invoke_generator import LinuxInvokeGenerator
from jarvis.agent.linux_task_judger import LinuxTaskJudger
'''
Made By WZM & DZC
target: use jarvis lib code to generate pipeline
'''
# environment
environment = PythonEnv()
# path of action lib
action_lib_path = "../jarvis/action_lib"
# use to look up existed skill code and extract information
agent = OpenAIAgent(config_path="./config.json")
# use to create a new skill code
skillCreator = LinuxSkillCreator(config_path="./config.json")
# use to generate the invoke code of the python tool class
invokeGenerator = LinuxInvokeGenerator(config_path="./config.json")
# use to judge wheter the task can be executed
taskJudger = LinuxTaskJudger(config_path="./config.json")
# use to amend the code
skillAmender = LinuxSkillAmend(config_path="./config.json")

response = '''
Thought: In order to solve this task, first create a folder named test2, then create a file named sth2.txt in the folder directory, and finally write the text "hello world" into it. We can parse the above steps into the following actions and corresponding descriptions.

Actions: 
1. <action>create_folder</action> <description>create a folder which is named test2 under the default working directory</description>
2. <action>create_file</action> <description>create a txt file which is named sth2.txt under a directory named test2 which is under the working directory.Then Write hello world in it.</description>
Check local action_lib, the required action code is in the library, according to the function description in the code, combined with the information provided by the user, You can instantiate classes for different tasks.

'''

action = agent.extract_action(response, begin_str='<action>', end_str='</action>')
task_description = agent.extract_action(response, begin_str='<description>', end_str='</description>')

# loop all the subtasks
for a,t in zip(action,task_description):
    # create python tool class code
    msg = skillCreator.format_message(task_name=a,task_description=t,working_dir=environment.working_dir)
    code = skillCreator.extract_python_code(msg)
    print(code)

    # create the invoke code
    msg_invoke = invokeGenerator.invoke_generator(code, t)
    print(msg_invoke)
    invoke = agent.extract_action(msg_invoke, begin_str='<invoke>', end_str='</invoke>')[0]
    code = code + '\n' + invoke

    # execute the tool code
    state = environment.step(code)
    print(state)

    # check whether the code runs correctly, if not, amend the code
    need_amend = False
    trial_times = 0
    critique = ""
    if state.error == None:
        judge_result = taskJudger.judge(code, t, state.result, state.pwd, state.ls)
        critique = judge_result['reasoning']
        if judge_result['judge'] == False:
            print("critique:{}".format(critique))
            need_amend = True
    else:
        need_amend = True
    # amend code and recheck
    current_code = code
    while (trial_times < 3) and (need_amend == True):
        trial_times += 1
        print("current amend times: {}".format(trial_times))
        amend_result = skillAmender.amend_code(current_code, t, state.error, state.result, state.pwd, state.ls, critique)
        print(amend_result)
        new_code = skillAmender.extract_python_code(amend_result)
        current_code = new_code
        state = environment.step(current_code)
        print(state)
        # recheck
        if state.error == None:
            judge_result = taskJudger.judge(current_code, t, state.result, state.pwd, state.ls)
            critique = judge_result['reasoning']
            if judge_result['judge'] == True:
                need_amend = False
                break
            print("critique:{}".format(critique))
        else:
            need_amend = True
    # save code or warning
    if need_amend == True:
        print("I can't Do this Task!!")
    else:
        # save to action lib
        file_path = action_lib_path + '/' + a + '.py'
        with open(file_path, "w") as file:
            lines = current_code.strip().splitlines()
            if lines:
                # remove the invoke code of the python file
                lines.pop()
            final_code = '\n'.join(lines)
            file.write(final_code)
