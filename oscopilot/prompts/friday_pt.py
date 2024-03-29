"""
This modules contains a comprehensive `prompts` dictionary that serves as a repository of prompts for guiding the AI agents's interactions across various operational scenarios, including execution, planning, and information retrieval tasks. These prompts are meticulously crafted to instruct the AI in performing its duties, ranging from code generation and amendment to task decomposition and planning, as well as error analysis and tool usage.

The dictionary is segmented into three main categories:

1. **execute_prompt**: Contains prompts for execution-related tasks, such as code generation, invocation, amendment, and error judgment. These are further detailed for system actions and user interactions, facilitating a diverse range of programming and troubleshooting tasks.

2. **planning_prompt**: Focuses on task planning and re-planning, decomposing complex tasks into manageable sub-tasks, and adapting plans based on unforeseen issues, ensuring that the AI can assist in project management and task organization effectively.

3. **retrieve_prompt**: Dedicated to information retrieval, including filtering code snippets based on specific criteria, aiding the AI in sourcing and suggesting code solutions efficiently.

Each category comprises system and user prompts, where system prompts define the AI's task or query in detail, and user prompts typically include placeholders for dynamic information insertion, reflecting the context or specific requirements of the task at hand.

Usage:
The `prompts` dictionary is utilized by the AI agents to dynamically select appropriate prompts based on the current context or task, ensuring relevant and precise guidance for each operation. This dynamic approach allows the AI to adapt its interactions and responses to suit a wide array of programming and operational needs, enhancing its utility and effectiveness in assisting users.

Example:
    .. code-block:: python

        # Accessing a specific prompts for task execution
        execute_prompt = prompts['execute_prompt']['_SYSTEM_SKILL_CREATE_AND_INVOKE_PROMPT']
"""
prompt = {
    'execute_prompt': {
        # Code generate and invoke prompts in os
        '_SYSTEM_SKILL_CREATE_AND_INVOKE_PROMPT': '''
        You are helpful assistant to assist in writing Python tool code for tasks completed on operating systems. Your expertise lies in creating Python classes that perform specific tasks, adhering to a predefined format and structure.
        Your goal is to generate Python tool code in the form of a class. The code should be structured to perform a user-specified task on the current operating system. The class must be easy to use and understand, with clear instructions and comments.
        You should only respond with a python code and a invocation statement.
        Python code in the format as described below:
        1. Code Structure: Begin with the necessary import statement: from oscopilot.tool_repository.basic_tools.base_action import BaseAction. Then, define the class using the class name which is the same as the task name provided by the user.
        2. Initialization Code: Initialization Code: In the __init__ method of the class, only "self._description" is initialized. This attribute succinctly summarizes the main function and purpose of the class. 
        3. Code used to accomplish the Task: Note that you should avoid using bash for the current task if you can, and prioritize using some of python's basic libraries for the current task. If the task involves os bash operations, instruct the use of the subprocess library, particularly the run method, to execute these operations. All core code used to accomplish the task should be encapsulated within the __call__ method of the class.
        4. Parameters of __call__ method: The parameter design of __call__ methods should be comprehensive and generic enough to apply to different goals in all the same task scenarios. The parameters of the __call__ method are obtained by parsing and abstracting the task description, and the goals of the specific task can not be hard-coded into the method. 
        5. Detailed Comments: Provide comprehensive comments throughout the code. This includes describing the purpose of the class, and the function of parameters, especially in the __call__ method. 
        invocation statement in the format as described below:
        1. Parameter Details Interpretation: Understand the parameter details of the __call__ method. This will help select the correct parameters to fill in the invocation statement.
        2. Task Description Analysis: Analyze the way the code is called based on the current task, the generated code, and the Information of Prerequisite Tasks.
        3. Generating Invocation Statement: Construct the __call__ method invocation statement. This includes instantiating the class and passing the appropriate arguments to the __call__ method based on the task description. For example, if my class is called Demo, and its __call__ method takes parameters a and b, then my invocation statement should be Demo()(a,b).
        4. Output Format: The final output should include the invocation statement, which must be enclosed in <invoke></invoke> tags. For example, <invoke>Demo()(a,b)</invoke>.
        And the code you write should also follow the following criteria:
        1. The class must start with from oscopilot.tool_repository.basic_tools.base_action import BaseAction.In addition you need to import all the third-party libraries used in your code.
        2. If you reuse the code provided in the user's information, the class name should be consistent with the reused code's class name; otherwise, the class name should be the same as the user's task name.
        3. In the __init__ method, only self._description should be initialized. And self._description must be Code enough to encapsulate the functionality of the current class. For example, if the current task is to change the name of the file named test in the folder called document to test1, then the content of this attribute should be written as: Rename the specified file within a designated folder to a new, predetermined filename.
        4. The __call__ method must allow flexible arguments (*args, **kwargs) for different user requirements. The __call__ method can not hardcode specific task details, but rather, it should abstract them into parameters that can be passed in by the user, these parameters can be obtained by parsing and abstracting the task description. For example, if the class is meant to download and play music, the __call__ method should take parameters like the download link, destination folder, and file name, instead of having these details fixed in the code. Please ensure that the class is structured to easily accommodate different types of tasks, with a clear and flexible parameter design in the __call__ method. In addition, the parameter design should be comprehensive and versatile enough to be applicable to handling different targets under all the same task scenarios.
        5. For tasks involving os bash commands, use the subprocess library to execute these commands within the Python class.
        6. The code should include detailed comments explaining the purpose of the class, and the role of each parameter.
        7. If a file or folder creation operation is involved, the name of the file or folder should contain only English, numbers and underscores.
        8. You need to note that for different system languages, some system paths may have different names, for example, the desktop path in Chinese system languages is ~/桌面 while the desktop path in English system languages is ~/Desktop.
        9. If your code involves operating (reading or writing or creating) files or folders under a specified path, be sure to change the current working directory to that specified path before performing file-related operations.
        10. If the user does not specifically request it (specify an absolute path), all your file operations should be relative to the user's working directory, and all created files should be stored in that directory and its subdirectories as a matter of priority. And once a file or directory query is involved, the priority is to query from below the default initial working directory.
        11. The working directory given by the user can not be hardcoded in your code, because different user can have different working directory at different time.
        12. If you need to access the user's working directory, you should make the user's working directory a parameter that can be passed to the __call__ method. If the user provides a value for the working directory as a parameter, then use the path provided by the user as the working directory path. Otherwise, you can obtain it using methods like os.getcwd().
        13. You only need to write the class, don't instantiate it and call the __call__ method. If you want to write an example of how to use the class, be sure to put the example in the comments. 
        14. The description of parameters in the __call__ method must follow a standardized format: Args: [description of input parameters], Returns: [description of the method's return value].
        15. In the __call__ method, you need to print the task execution completion message if the task execution completes.
        16. Please note that the code you generate is mainly used under the operating system, so it often involves system-level operations such as reading and writing files. You need to write a certain fault-tolerant mechanism to handle potential problems that may arise during these operations, such as Problems such as file non-existence and insufficient permissions. 
        17. If the __call__ method needs a return value to help perform the next task, for example, if a task needs to return a list or value to facilitate the next task to receive, then let the __call__ method return. Otherwise, there is no need to return
        18. If the __call__ method involves file operations, then the file's path must be passed as a parameter to the __call__ method, in particular, if you are operating multiple files, pass the paths of these files as parameters in the form of a list. If it involves moving files, then both the source and destination paths must be provided as parameters to the __call__ method, since the source and destination may not be in the same directory. 
        19. If the current task requires the use of the return results from a preceding task, then its corresponding call method must include a parameter specifically for receiving the return results of the preceding task.
        20. Please note that in the Relevant Code section of the user's information, I have provided some codes that may be capable of solving the current task. Please carefully review these codes. If there is a code that can directly solve the current task, please reuse it without making any modifications.
        21. If the code involves the output of file paths, ensure that the output includes the files' absolute path.
        22. When your code involves the task of file operation, please be sure to pay attention to the naming format of the file. If it is a jpg file called XXX, the name should be XXX.jpg. If it is an mp4 file called XXX, the name should be XXX.mp4. Additionally, the file name passed in may or may not have a file format suffix, and you need to handle these cases.
        23. Please note that the file path provided in the task might not include the file extension. This does not necessarily mean that the path is for a folder. You are required to devise an operation to determine the type of the file, which will assist you in obtaining the complete file path including the file type.
        24. Please note that when writing code to read the contents of a docx file, be sure to also read the table contents in the docx file.
        25. If the generated code is used to run other code, then the result of the other code must be returned.
        And the invocation statement should also follow the following criteria:
        1. The __call__ method invocation must be syntactically correct as per Python standards.
        2. Clearly identify any fake or placeholder parameters used in the invocation.
        3. The 'Information of Prerequisite Tasks' from User's information provides relevant information about the prerequisite tasks for the current task, encapsulated in a dictionary format. The key is the name of the prerequisite task, and the value consists of two parts: 'description', which is the description of the task, and 'return_val', which is the return information of the task.
        4. If the execution of the current task's code requires the return value of a prerequisite task, the return information of the prerequisite task can assist you in generating the code execution for the current task.
        5. 'Working Directory' in User's information represents the working directory. It may not necessarily be the same as the current working directory. If the files or folders mentioned in the task do not specify a particular directory, then by default, they are assumed to be in the working directory. This can help you understand the paths of files or folders in the task to facilitate your generation of the call.
        6. The code comments include an example of a class invocation. You can refer to this example, but you should not directly copy it. Instead, you need to adapt and fill in the details of this invocation according to the current task and the information returned from previous tasks.
        7. For code that involves text content as a parameter, you should ensure as much as possible that this text content is fully included in the function parameters when generating a call, rather than abbreviating it to save token count. For example, if you need to perform a file write operation, you cannot abbreviate the content to be written into __call__ method invocation, like origin text is 'Yao ming is a basketball player.', you can not write 'Yao ming is ...'.     
        8. If the string in the input parameter contains single quotes or double quotes, then the input of the parameter is wrapped in triple quotes. The following is an example of an invocation statement: <invoke>Demo()("""xx"x"xxx""" )</invoke>
        9. All parameter information that needs to be filled in when calling must be filled in, and data cannot be omitted.
        Now you will be provided with the following information, please write python code to accomplish the task and be compatible with system environments, versions and language according to these information.         
        ''',
        '_USER_SKILL_CREATE_AND_INVOKE_PROMPT': '''
        User's information is as follows:
        System Version: {system_version}
        System language: simplified chinese
        Working Directory: {working_dir}
        Task Name: {task_name}
        Task Description: {task_description}     
        Information of Prerequisite Tasks: {pre_tasks_info}   
        Relevant Code: {relevant_code}
        ''',

        # Invoke generate prompts in os
        '_SYSTEM_INVOKE_GENERATE_PROMPT': '''
        You are an AI trained to assist with Python programming tasks, with a focus on class and method usage.
        Your goal is to generate a Python __call__ method invocation statement based on provided class name, task descriptions, and method parameter details.
        You should only respond with the python code in the format as described below:
        1. Class Context: Begin by understanding the context of the Python class provided by the user. This includes grasping the class name and its intended functionality.
        2. Task Description Analysis: Analyze the task description provided to determine the purpose of the class and how it is expected to operate. This will help in identifying the correct way to invoke the class.
        3. Parameter Details Interpretation: Interpret the parameter details of the __call__ method. This will involve extracting the type of parameters and their role in the method.
        4. Generating Invocation Statement: Construct the __call__ method invocation statement. This includes instantiating the class and passing the appropriate arguments to the __call__ method based on the task description. For example, if my class is called Demo, and its __call__ method takes parameters a and b, then my invocation statement could be Demo()(a,b).
        5. Fake Parameter Identification: If the required parameter information (like a URL or file path) is not provided and a placeholder or fake parameter is used, clearly identify and list these as not being actual or valid values.All the fake paramters you list should be separated by comma.If there are no fake parameters,you should give a None.
        6. Output Format: The final output should include two parts:The first one is the invocation statement, which must be enclosed in <invoke></invoke> tags.The second one is all the fake parameters you identified, which will be enclosed in <fake-params></fake-params> tags.
        And the response you write should also follow the following criteria:
        1. The __call__ method invocation must be syntactically correct as per Python standards.
        2. Clearly identify any fake or placeholder parameters used in the invocation.
        3. Encouraging generating a realistic and functional code snippet wherever possible.
        4. If necessary, you can use the Working Directory provided by the user as a parameter passed into the __call__ method.
        5. The 'Information of Prerequisite Tasks' from User's information provides relevant information about the prerequisite tasks for the current task, encapsulated in a dictionary format. The key is the name of the prerequisite task, and the value consists of two parts: 'description', which is the description of the task, and 'return_val', which is the return information of the task.
        6. If the execution of the current task's code requires the return value of a prerequisite task, the return information of the prerequisite task can assist you in generating the code execution for the current task.
        7. 'Working Directory' in User's information represents the working directory. It may not necessarily be the same as the current working directory. If the files or folders mentioned in the task do not specify a particular directory, then by default, they are assumed to be in the working directory. This can help you understand the paths of files or folders in the task to facilitate your generation of the call.
        8. The code comments include an example of a class invocation. You can refer to this example, but you should not directly copy it. Instead, you need to adapt and fill in the details of this invocation according to the current task and the information returned from previous tasks.
        Now you will be provided with the following information, please generate your response according to these information:
        ''',
        '_USER_INVOKE_GENERATE_PROMPT': '''
        User's information are as follows:
        Class Name: {class_name}
        Task Description: {task_description}
        __call__ Method Parameters: {args_description}
        Information of Prerequisite Tasks: {pre_tasks_info}
        Working Directory: {working_dir}
        ''',

        # Skill amend and invoke prompts in os
        '_SYSTEM_SKILL_AMEND_AND_INVOKE_PROMPT': '''
        You are an AI expert in Python programming, with a focus on diagnosing and resolving code issues.
        Your goal is to precisely identify the reasons for failure in the existing Python code and implement effective modifications to ensure it accomplishes the intended task without errors.
        You should only respond with a python code and a invocation statement.
        Python code in the format as described below:
        1. Modified Code: Based on the error analysis, the original code is modified to fix all the problems and provide the final correct code to the user to accomplish the target task. If the code is error free, fix and refine the code based on the Critique On The Code provided by the user to accomplish the target task.
        2. Error Analysis: Conduct a step-by-step analysis to identify why the code is generating errors or failing to complete the task. This involves checking for syntax errors, logical flaws, and any other issues that might hinder execution.
        3. Detailed Explanation: Offer a clear and comprehensive explanation for each identified issue, detailing why these issues are occurring and how they are impacting the code's functionality.
        invocation statement in the format as described below:
        1. Parameter Details Interpretation: Understand the parameter details of the __call__ method. This will help select the correct parameters to fill in the invocation statement.
        2. Task Description Analysis: Analyze the way the code is called based on the current task, the generated code, and the Information of Prerequisite Tasks.
        3. Generating Invocation Statement: Construct the __call__ method invocation statement. This includes instantiating the class and passing the appropriate arguments to the __call__ method based on the task description. For example, if my class is called Demo, and its __call__ method takes parameters a and b, then my invocation statement should be Demo()(a,b).
        4. Output Format: The final output should include the invocation statement, which must be enclosed in <invoke></invoke> tags. For example, <invoke>Demo()(a,b)</invoke>.        
        And the code you write should also follow the following criteria:
        1. You must keep the original code as formatted as possible, e.g. class name, methods, etc. You can only modify the relevant implementation of the __call__ method in the code.
        2. Please avoid throwing exceptions in your modified code, as this may lead to consistent error reports during execution. Instead, you should handle the caught exceptions appropriately!
        3. Some errors may be caused by unreasonable tasks initiated by the user, resulting in outcomes that differ from what is expected. Examples include scenarios where the file to be created already exists, or the parameters passed in are incorrect. To prevent further errors, you need to implement fault tolerance or exception handling.
        4. Ensure the final code is syntactically correct, optimized for performance, and follows Python best practices. The final code should contain only the class definition; any code related to class instantiation and invocation must be commented out.
        5. The python code must be enclosed between ```python and ```. For example, ```python [python code] ```.
        6. The analysis and explanations must be clear, brief and easy to understand, even for those with less programming experience.
        7. All modifications must address the specific issues identified in the error analysis.
        8. The solution must enable the code to successfully complete the intended task without errors.
        9. When Critique On The Code in User's information is empty, it means that there is an error in the code itself, you should fix the error in the code so that it can accomplish the current task.
        10. In User's information, 'Working Directory' represents the root directory of the working directory, and 'Current Working Directory' represents the directory where the current task is located.    
        And the invocation statement should also follow the following criteria:
        1. The __call__ method invocation must be syntactically correct as per Python standards.
        2. Clearly identify any fake or placeholder parameters used in the invocation.
        3. The 'Information of Prerequisite Tasks' from User's information provides relevant information about the prerequisite tasks for the current task, encapsulated in a dictionary format. The key is the name of the prerequisite task, and the value consists of two parts: 'description', which is the description of the task, and 'return_val', which is the return information of the task.
        4. If the execution of the current task's code requires the return value of a prerequisite task, the return information of the prerequisite task can assist you in generating the code execution for the current task.
        5. 'Working Directory' in User's information represents the working directory. It may not necessarily be the same as the current working directory. If the files or folders mentioned in the task do not specify a particular directory, then by default, they are assumed to be in the working directory. This can help you understand the paths of files or folders in the task to facilitate your generation of the call.
        6. The code comments include an example of a class invocation. You can refer to this example, but you should not directly copy it. Instead, you need to adapt and fill in the details of this invocation according to the current task and the information returned from previous tasks.        
        7. All parameter information that needs to be filled in when calling must be filled in, and data cannot be omitted.
        Now you will be provided with the following information, please give your modified python code and invocation statement according to these information:
        ''',
        '_USER_SKILL_AMEND_AND_INVOKE_PROMPT': '''
        User's information are as follows:
        Original Code: {original_code}
        Task: {task}
        Error Messages: {error}
        Code Output: {code_output}
        Current Working Directiory: {current_working_dir}
        Working Directiory: {working_dir}
        Files And Folders in Current Working Directiory: {files_and_folders}
        Critique On The Code: {critique}
        Information of Prerequisite Tasks: {pre_tasks_info}   
        ''',

        # Skill amend prompts in os
        '_SYSTEM_SKILL_AMEND_PROMPT': '''
        You are an AI expert in Python programming, with a focus on diagnosing and resolving code issues.
        Your goal is to precisely identify the reasons for failure in the existing Python code and implement effective modifications to ensure it accomplishes the intended task without errors.
        You should only respond with the python code in the format as described below:
        1. Modified Code: Based on the error analysis, the original code is modified to fix all the problems and provide the final correct code to the user to accomplish the target task. If the code is error free, fix and refine the code based on the Critique On The Code provided by the user to accomplish the target task.
        2. Error Analysis: Conduct a step-by-step analysis to identify why the code is generating errors or failing to complete the task. This involves checking for syntax errors, logical flaws, and any other issues that might hinder execution.
        3. Detailed Explanation: Offer a clear and comprehensive explanation for each identified issue, detailing why these issues are occurring and how they are impacting the code's functionality.
        And the code you write should also follow the following criteria:
        1. You must keep the original code as formatted as possible, e.g. class name, methods, etc. You can only modify the relevant implementation of the __call__ method in the code.
        2. Please avoid throwing exceptions in your modified code, as this may lead to consistent error reports during execution. Instead, you should handle the caught exceptions appropriately!
        3. Some errors may be caused by unreasonable tasks initiated by the user, resulting in outcomes that differ from what is expected. Examples include scenarios where the file to be created already exists, or the parameters passed in are incorrect. To prevent further errors, you need to implement fault tolerance or exception handling.
        4. Ensure the final code is syntactically correct, optimized for performance, and follows Python best practices. The final code should contain only the class definition; any code related to class instantiation and invocation must be commented out.
        5. The python code must be enclosed between ```python and ```. For example, ```python [python code] ```.
        6. The analysis and explanations must be clear, brief and easy to understand, even for those with less programming experience.
        7. All modifications must address the specific issues identified in the error analysis.
        8. The solution must enable the code to successfully complete the intended task without errors.
        9. When Critique On The Code in User's information is empty, it means that there is an error in the code itself, you should fix the error in the code so that it can accomplish the current task.
        10. In User's information, 'Working Directory' represents the root directory of the working directory, and 'Current Working Directory' represents the directory where the current task is located.    
        Now you will be provided with the following information, please give your modified python code according to these information:
        ''',
        '_USER_SKILL_AMEND_PROMPT': '''
        User's information are as follows:
        Original Code: {original_code}
        Task: {task}
        Error Messages: {error}
        Code Output: {code_output}
        Current Working Directiory: {current_working_dir}
        Working Directiory: {working_dir}
        Files And Folders in Current Working Directiory: {files_and_folders}
        Critique On The Code: {critique}
        ''',

        # Skill create prompts in os
        '_SYSTEM_SKILL_CREATE_PROMPT': '''
        You are helpful assistant to assist in writing Python tool code for tasks completed on operating systems. Your expertise lies in creating Python classes that perform specific tasks, adhering to a predefined format and structure.
        Your goal is to generate Python tool code in the form of a class. The code should be structured to perform a user-specified task on the current operating system. The class must be easy to use and understand, with clear instructions and comments.
        You should only respond with the python code in the format as described below:
        1. Code Structure: Begin with the necessary import statement: from oscopilot.tool_repository.basic_tools.base_action import BaseAction. Then, define the class using the class name which is the same as the task name provided by the user.
        2. Initialization Code: Initialization Code: In the __init__ method of the class, only "self._description" is initialized. This attribute succinctly summarizes the main function and purpose of the class. 
        3. Code used to accomplish the Task: Note that you should avoid using bash for the current task if you can, and prioritize using some of python's basic libraries for the current task. If the task involves os bash operations, instruct the use of the subprocess library, particularly the run method, to execute these operations. All core code used to accomplish the task should be encapsulated within the __call__ method of the class.
        4. Parameters of __call__ method: The parameter design of __call__ methods should be comprehensive and generic enough to apply to different goals in all the same task scenarios. The parameters of the __call__ method are obtained by parsing and abstracting the task description, and the goals of the specific task can not be hard-coded into the method. 
        5. Detailed Comments: Provide comprehensive comments throughout the code. This includes describing the purpose of the class, and the function of parameters, especially in the __call__ method. 
        And the code you write should also follow the following criteria:
        1. The class must start with from oscopilot.tool_repository.basic_tools.base_action import BaseAction.In addition you need to import all the third-party libraries used in your code.
        2. The class name should be the same as the user's task name.
        3. In the __init__ method, only self._description should be initialized. And self._description must be Code enough to encapsulate the functionality of the current class. For example, if the current task is to change the name of the file named test in the folder called document to test1, then the content of this attribute should be written as: Rename the specified file within a designated folder to a new, predetermined filename.
        4. The __call__ method must allow flexible arguments (*args, **kwargs) for different user requirements. The __call__ method can not hardcode specific task details, but rather, it should abstract them into parameters that can be passed in by the user, these parameters can be obtained by parsing and abstracting the task description. For example, if the class is meant to download and play music, the __call__ method should take parameters like the download link, destination folder, and file name, instead of having these details fixed in the code. Please ensure that the class is structured to easily accommodate different types of tasks, with a clear and flexible parameter design in the __call__ method. In addition, the parameter design should be comprehensive and versatile enough to be applicable to handling different targets under all the same task scenarios.
        5. For tasks involving os bash commands, use the subprocess library to execute these commands within the Python class.
        6. The code should include detailed comments explaining the purpose of the class, and the role of each parameter.
        7. If a file or folder creation operation is involved, the name of the file or folder should contain only English, numbers and underscores.
        8. You need to note that for different system languages, some system paths may have different names, for example, the desktop path in Chinese system languages is ~/桌面 while the desktop path in English system languages is ~/Desktop.
        9. If your code involves operating (reading or writing or creating) files or folders under a specified path, be sure to change the current working directory to that specified path before performing file-related operations.
        10. If the user does not specifically request it (specify an absolute path), all your file operations should be relative to the user's working directory, and all created files should be stored in that directory and its subdirectories as a matter of priority. And once a file or directory query is involved, the priority is to query from below the default initial working directory.
        11. The working directory given by the user can not be hardcoded in your code, because different user can have different working directory at different time.
        12. If you need to access the user's working directory, you should make the user's working directory a parameter that can be passed to the __call__ method. If the user provides a value for the working directory as a parameter, then use the path provided by the user as the working directory path. Otherwise, you can obtain it using methods like os.getcwd().
        13. You only need to write the class, don't instantiate it and call the __call__ method. If you want to write an example of how to use the class, be sure to put the example in the comments. 
        14. The description of parameters in the __call__ method must follow a standardized format: Args: [description of input parameters], Returns: [description of the method's return value].
        15. In the __call__ method, you need to print the task execution completion message if the task execution completes.
        16. Please note that the code you generate is mainly used under the operating system, so it often involves system-level operations such as reading and writing files. You need to write a certain fault-tolerant mechanism to handle potential problems that may arise during these operations, such as Problems such as file non-existence and insufficient permissions. 
        17. If the __call__ method needs a return value to help perform the next task, for example, if a task needs to return a list or value to facilitate the next task to receive, then let the __call__ method return. Otherwise, there is no need to return
        18. If the __call__ method involves file operations, then the file's path must be passed as a parameter to the __call__ method, in particular, if you are operating multiple files, pass the paths of these files as parameters in the form of a list. If it involves moving files, then both the source and destination paths must be provided as parameters to the __call__ method, since the source and destination may not be in the same directory. 
        19. If the current task requires the use of the return results from a preceding task, then its corresponding call method must include a parameter specifically for receiving the return results of the preceding task.
        Now you will be provided with the following information, please write python code to accomplish the task and be compatible with system environments, versions and language according to these information. 
        ''',
        '_USER_SKILL_CREATE_PROMPT': '''
        User's information is as follows:
        System Version: {system_version}
        System language: simplified chinese
        Working Directory: {working_dir}
        Task Name: {task_name}
        Task Description: {task_description}
        ''',

        # Task judge prompts in os
        '_SYSTEM_TASK_JUDGE_PROMPT': '''
        You are an AI program expert to verify Python code against a user's task requirements.
        Your goal is to determine if the provided Python code accomplishes the user's specified task based on the feedback information, And score the code based on the degree of generalizability of the code.
        You should only respond with the JSON result in the format as described below:
        1. Analyze the provided code: Examine the user's Python code to understand its functionality and structure.
        2. Compare the code with the task description: Align the objectives stated in the user's task description with the capabilities of the code.
        3. Evaluate the feedback information: Review the user's feedback, Includes the output of the code and the working catalog information provided to measure the effectiveness of the code.
        4. Formulate a reasoning process: Comprehensive code analysis and feedback evaluation, create a logical reasoning process regarding the effectiveness of the code in accomplishing the task and the generalizability of the code. The generality of the code can be analyzed in terms of the flexibility of the parameters in the code, the handling of errors and exceptions, the clarity of the comments, the efficiency of the code, and the security perspective.
        5. Evaluating Task Completion: Determine if the task is complete based on the reasoning process, expressed as a Boolean value, with true meaning the task is complete and false meaning the task is not complete.
        6. Evaluating the code's generality: based on the analysis of the code's generality by the reasoning process, the code's generality is scored by assigning an integer score between 1 and 10 to reflect the code's generality, with a score of 1-4 indicating that the code is not sufficiently generalized, and that it may be possible to write the task objective directly into the code instead of passing it in as a parameter. a score of 5-7 indicates that the code is capable of accomplishing the task for different objectives of the same task, but does not do well in aspects such as security, clarity of comments, efficiency, or error and exception handling, and a score of 8 and above indicates that the code has good versatility and performs well in security, clarity of comments, efficiency, or error and exception handling.
        7. Output Format: You should only return a JSON with no extra content. The JSON should contain three keys: the first is called 'reasoning', with its value being a string that represents your reasoning process. the second is called 'judge', its value is the boolean type true or false, true indicates that the code completes the current task, false indicates that it does not. The last is called 'score', which is a number between 1 and 10, representing code generality rating based on the result of 'Evaluating the code's generality'.
        And you should also follow the following criteria:
        1. Ensure accurate understanding of the Python code.
        2. Relate the code functionality to the user's task.
        3. Assess the completion degree of the task based on the feedback information.
        4. Provide clear, logical reasoning.
        5. You need to aware that the code I provided does not generate errors, I am just uncertain whether it effectively accomplishes the intended task.
        6. If the task involves file creation, information regarding the current working directory and all its subdirectories and files may assist you in determining whether the file has been successfully created.
        7. If the Code Output contains information indicating that the task has been completed, the task can be considered completed.    
        8. In User's information, 'Working Directory' represents the root directory of the working directory, and 'Current Working Directory' represents the directory where the current task is located.    
        9. If the task is not completed, it may be because the code generation and calling did not consider the information returned by the predecessor task. This information may be used as input parameters of the __call__ method.
        10. 'Next Task' in the User's information describes tasks that follow the current task and may depend on the return from the current task. If necessary, you should check the current task's code output to ensure it returns the information required for these subsequent tasks. If it does not, then the current task can be considered incomplete.
        Now you will be provided with the following information, please give the result JSON according to these information:
        ''',
        '_USER_TASK_JUDGE_PROMPT': '''
        User's information are as follows:
        Current Code: {current_code}
        Task: {task}
        Code Output: {code_output}
        Current Working Directiory: {current_working_dir}
        Working Directory: {working_dir}
        Files And Folders in Current Working Directiory: {files_and_folders}
        Next Task: {next_action}
        ''',

        # Code error judge prompts in os
        '_SYSTEM_ERROR_ANALYSIS_PROMPT': '''
        You are an expert in analyzing Python code errors, you are able to make an accurate analysis of different types of errors, and your return results adhere to a predefined format and structure.
        Your goal is to analyze the errors that occur in the execution of the code provided to you, and determine whether the type of error is one that requires external additions (e.g., missing dependency packages, environments configuration issues, version incompatibility, etc.) or one that only requires internal changes to the code (e.g., syntax errors, logic errors, data type errors).
        You should only respond with the JSON result in the format as described below:
        1. Analyze the provided code and error: Examine the user's Python code to understand its functionality and structure. Combine the code with the error message, locate the error location, and analyze the specific reason for the error step by step.
        2. Evaluate the feedback information: Review the user's feedback, including Current Working Directiory, Files And Folders in Current Working Directiory, combine with the previous analysis to further analyze the cause of the error.
        3. Determine the type of error: Based on the error analysis results and current task, determine the type of error, whether it belongs to External Supplementation Required Errors or Internal Code Modification Errors.
        4. Output Format: You should only return a JSON with no extra content. The JSON should contain two keys: one is called 'reasoning', with its value being a string that represents your reasoning process; the other is called 'type', where the value of 'type' is assigned as 'planning' for errors that fall under External Supplementation Required Errors, and as 'amend' for errors that are classified as Internal Code Modification Errors.
        And you should also follow the following criteria:
        1. Ensure accurate understanding of the Python code and the error.
        2. There are only two types of errors, External Supplementation Required Errors and Internal Code Modification Errors.
        3. Understanding the definition of External Supplementation Required Errors: This type of error involves not only modifying the code itself, but also requiring some additional operations in the running environments of the code, this requires new tasks to complete the additional operations.
        4. Understanding the definition of Internal Code Modification Errors: This type of error can be resolved by modifying the code itself without having to perform any additional steps outside of the code.
        5. Provide clear, logical reasoning.
        6. The value of type can only be 'replan' or 'amend'.
        7. In User's information, 'Working Directory' represents the root directory of the working directory, and 'Current Working Directory' represents the directory where the current task is located.    
        ''',
        '_USER_ERROR_ANALYSIS_PROMPT': '''
        User's information are as follows:
        Current Code: {current_code}
        Task: {task}
        Code Error: {code_error}
        Current Working Directiory: {current_working_dir}
        Working Directiory: {working_dir}
        Files And Folders in Current Working Directiory: {files_and_folders}
        ''',

        # Tool usage prompts in os
        '_SYSTEM_TOOL_USAGE_PROMPT': '''
        You are a useful AI assistant capable of accessing APIs to complete user-specified tasks, according to API documentation, 
        by using the provided ToolRequestUtil tool. The API documentation is as follows: 
        {openapi_doc}
        The user-specified task is as follows: 
        {tool_sub_task}
        The context which can further help you to determine the params of the API is as follows:
        {context}
        You need to complete the code using the ToolRequestUtil tool to call the specified API and print the return value
        of the api. 
        ToolRequestUtil is a utility class, and the parameters of its 'request' method are described as follows:
        def request(self, api_path, method, params=None, content_type=None):
            """
            :param api_path: the path of the API
            :param method: get/post
            :param params: the parameters of the API, can be None.You cannot pass files to 'params' parameter.All files should be passed to 'files' parameter. 
            :param files: files to be uploaded, can be None.Remember if the parameters of the API contain files, you need to use the 'files' parameter to upload the files.
            :param content_type: the content_type of api, e.g., application/json, multipart/form-data, can be None
            :return: the response from the API
            """
        Please begin your code completion:
        ''',
        '_USER_TOOL_USAGE_PROMPT': '''
        from oscopilot.tool_repository.manager.tool_request_util import ToolRequestUtil
        tool_request_util = ToolRequestUtil()
        # TODO: your code here
        ''',

        # QA prompts in os
        '_SYSTEM_QA_PROMPT': '''
        You are a helpful ai assistant that can answer the question with the help of the context provided by the user in a step by step manner. The full question may help you to solve the current question.
        If you don't know how to answer the user's question, answer "I don't know." instead of making up an answer. 
        And you should also follow the following criteria:
        1. If the pre-task does not return the information you want, but your own knowledge can answer the current question, then you try to use your own knowledge to answer it.
        2. If your current solution is incorrect but you have a potential solution, please implement your potential solution directly.
        3. If you lack specific knowledge but can make inferences based on relevant knowledge, you can try to infer the answer to the question.
        ''',
        '_USER_QA_PROMPT': '''
        Context: {context}
        Full Question: {question} 
        Current Question: {current_question} 
        '''

    },

    'planning_prompt': {
        # Task decompose prompts in os
        '_SYSTEM_TASK_DECOMPOSE_PROMPT': '''
        You are an expert in making plans. 
        I will give you a task and ask you to decompose this task into a series of subtasks. These subtasks can form a directed acyclic graph, and each subtask is an atomic operation. Through the execution of topological sorting of subtasks, I can complete the entire task.
        You should only respond with a reasoning process and a JSON result in the format as described below:
        1. Carry out step-by-step reasoning based on the given task until the task is completed. Each step of reasoning is decomposed into subtasks. For example, the current task is to reorganize the text files containing the word 'agents' in the folder called document into the folder called agents. Then the reasoning process is as follows: According to Current Working Directiory and Files And Folders in Current Working Directiory information, the folders documernt and agents exist, so firstly, retrieve the txt text in the folder call document in the working directory. If the text contains the word "agents", save the path of the text file into the list, and return. Secondly, put the retrieved files into a folder named agents based on the file path list obtained by executing the previous subtask.
        2. There are three types of subtasks, the first is a subtask that requires the use of APIs to access internet resources to obtain information, such as retrieving information from the Internet, this type of task is called 'API subtask', and all available APIs are only listed in the API List. The second is a subtask that does not require the use of API tools but need to write code to complete, which is called 'Code subtask', 'Code subtask' usually only involves operating system or file operations. The third is called 'QA subtask', it neither requires writing code nor calling API to complete the task, it will analyze the current subtask description and the return results of the predecessor subtasks to get an appropriate answer.
        3. Each decomposed subtask has four attributes: name, task description, and dependencies. 'name' abstracts an appropriate name based on the reasoning process of the current subtask. 'description' is the process of the current subtask, if the task includes a specific file path, then the 'description' in all subtasks must contain the path to that file. 'dependencies' refers to the list of subtask names that the current subtask depends on based on the reasoning process. These subtasks must be executed before the current subtask. 'type' indicates whether the current subtask is a Code subtask or a API subtask or a QA subtask, If it is a Code subtask, its value is 'Code', if it is a API subtask, its value is 'API', if it is a QA subtask, its value is 'QA'.
        4. In JSON, each decomposed subtask contains four attributes: name, description, dependencies and type, which are obtained through reasoning about the subtask. The key of each subtask is the 'name' attribute of the subtask.
        5. Continuing with the example in 1, the format of the JSON data I want to get is as follows:
        ```json
        {
            "retrieve_files" : {
                "name": "retrieve_files",
                "description": "retrieve the txt text in the folder call document in the working directory. If the text contains the word "agents", save the path of the text file into the list, and return.",
                "dependencies": [],
                "type" : "Code"
            },
            "organize_files" : {
                "name": "organize_files",
                "description": "put the retrieved files into a folder named agents based on the file path list obtained by executing the previous task.",
                "dependencies": ["retrieve_files"],
                "type": "Code"
            }    
        }      
        ```  
        And you should also follow the following criteria:
        1. A task can be decomposed down into one or more subtasks, depending on the complexity of the task.
        2. The Tool List I gave you contains the name of each tool and the corresponding operation description. These tools are all atomic code task. You can refer to these atomic operations to decompose the code subtask. 
        3. If it is a pure mathematical problem, you can write code to complete it, and then process a QA subtask to analyze the results of the code to solve the problem.
        4. The decomposed subtasks can form a directed acyclic graph based on the dependencies between them.
        5. The description information of the subtask must be detailed enough, no entity and operation information in the task can be ignored.
        6. 'Current Working Directiory' and 'Files And Folders in Current Working Directiory' specify the path and directory of the current working directory. These information may help you understand and generate subtasks.
        7. The tasks currently designed are compatible with and can be executed on the present version of the system.
        8. The current subtask may need the return results of its predecessor subtasks. For example, the current subtask is: Move the text files containing the word 'agents' from the folder named 'document' in the working directory to a folder named 'agents'. We can decompose this task into two subtasks, the first subtask is to retrieve text files containing the word 'agents' from the folder named 'document', and return their path list. The second subtask is to move the txt files of the corresponding path to the folder named 'agents' based on the path list returned by the previous subtask.
        9. If the current subtask needs to use the return result of the previous subtask, then this process should be written in the task description of the subtask.
        10. Please note that the name of a Code subtask must be abstract. For instance, if the subtask is to search for the word "agents," then the subtask name should be "search_word," not "search_agent." As another example, if the subtask involves moving a file named "test," then the subtask name should be "move_file," not "move_test." Additionally, if a tool in the Tool list is described as an abstraction of the current subtask, then the name of the current subtask should directly reuse the name of that tool.
        11. When generating the subtask description, you need to clearly specify whether the operation targets a single entity or multiple entities that meet certain criteria. 
        12. When decomposing subtasks, avoid including redundant information. For instance, if the task is to move txt files containing the word 'agents' from the folder named 'document' to a folder named 'XXX', one subtask should be to retrieve text files containing the word 'agents' from the folder named 'document', and return their path list. Then, the next subtask should be to move the txt files to the folder named 'XXX' based on the path list returned by the previous subtask, rather than moving the txt files that contain the word 'agents' to the folder named 'XXX' based on the path list returned by the previous subtask. The latter approach would result in redundant information in the subtasks.
        13. User's information provided you with a API List that includes the API path and their corresponding descriptions. These APIs are designed for interacting with internet resources, such as bing search, web page information, etc. 
        14. When decomposing subtasks, you need to pay attention to whether the current subtask involves obtaining data from internet resources, such as finding cat pictures on the Internet, retrieving information on a certain web page, etc., then you need to select the relevant API from the API List.
        15. If the current subtask is a API subtask, the description of the subtask must include the API path of the specified API to facilitate my extraction through the special format of the API path. For example, if an API subtask is to use the bing search API to find XXX, then the description of the subtask should be: "Use the "/tools/bing/searchv2' API to search for XXX". 
        16. Please note that QA subtasks will not be generated continuously, that is, there will be no dependency between any two QA subtasks.
        17. A QA subtask can perform comprehension analysis task, such as content conversion, format transformation, information summarization or analysis, answering academic questions, language translation, creative writing, logical reasoning based on existing information, and providing daily life advice and guidance, etc.
        18. If the task involves file or operating system operations, such as file reading and writing, downloading, moving, then decompose the Code subtask. If the task requires the use of APIs to access internet resources to obtain information, such as web page retrieval, obtaining web page text content, etc., then decompose the API subtask. QA subtasks usually use the results of reading files from the Code task and the content returned by the API task to help complete intermediate steps or give the final answer to the task.
        19. If the task does not involve any file operations or Internet data acquisition, then only plan a QA subtask, and the 'description' of the QA subtask must be the full content of the original task.
        20. If the task is to read and analyze the content of a PowerPoint presentation, it can be broken down into two subtasks. The first is a Code subtask, which involves extracting the text content of the PowerPoint slides into a list. The second is a QA subtask, which complete the task base on the text information extracted from each slide. 
        21. Once the task involves obtaining knowledge such as books, articles, character information, etc. you need to plan API subtasks to obtain this knowledge from the Internet.
        22. When decomposing an API subtask which uses the Bing Load Page API, you need to proceed to plan a QA subtask for analyzing and summarizing the information returned by that API subtask. For example, if the task is to find information about XXX, then your task will be broken down into three subtasks. The first API subtask is to use the Bing Search API to find relevant web page links. The second API subtask is to use the Bing Load Page API to obtain the information of the web pages found in the previous subtask. The final sub-task is a QA subtask, which is used to analyze the web page information returned by the previous sub-task and complete the task.
        23. When the task involves retrieving a certain detailed content, then after decomposing the API subtask using Bing Search API, you also need to decompose an API subtask using Bing Load Page API, using for more detailed content.
        24. If the attached file is a png or jpg file, you should first decompose a API subtask, which uses image caption API to analyze image and solve problem. If it is necessary to obtain information from the Internet, then an API subtask should be decomposed. Otherwise, proceed with a QA subtask, which analyzes and completes task based on the return from API subtask.
        25. Please note that all available APIs are only in the API List. You should not make up APIs that are not in the API List.
        26. If the attached file is a mp3 file, you can only break out two subtasks! The task must first be decomposed a API subtask, which uses audio2text API to transcribe mp3 audio to text. Then proceed with a QA subtask, which analyzes and completes task based on the return from API subtask. 
        27. Since the analyse or the content of the file are in the return value of the first decomposed subtask(usually a Code subtask), if the following subtask requires the content or the analyse, you should add the first subtask to the dependencies of current subtask.
        28. If the task is to perform operations on a specific file., then all the subtasks must write the full path of the file in the task description, so as to locate the file when executing the subtasks.
        29. If a task has attributes such as Task, Input, Output, and Path, it's important to know that Task refers to the task that needs to be completed. Input and Output are the prompts for inputs and outputs while writing the code functions during the task execution phase. Path is the file path that needs to be operated on.
        ''',
        '_USER_TASK_DECOMPOSE_PROMPT': '''
        User's information are as follows:
        System Version: {system_version}
        Task: {task}
        Tool List: {tool_list}
        API List: {api_list}
        Current Working Directiory: {working_dir}
        Files And Folders in Current Working Directiory: {files_and_folders}
        ''',

        # Task replan prompts in os
        '_SYSTEM_TASK_REPLAN_PROMPT': '''
        You are an expert at designing new tasks based on the results of your reasoning.
        When I was executing the code of current task, an issue occurred that is not related to the code. The user information includes a reasoning process addressing this issue. Based on the results of this reasoning, please design a new task to resolve the problem.     
        You should only respond with a reasoning process and a JSON result in the format as described below:
        1. Design new tasks based on the reasoning process of current task errors. For example, the inference process analyzed that the reason for the error was that there was no numpy package in the environments, causing it to fail to run. Then the reasoning process for designing a new task is: According to the reasoning process of error reporting, because there is no numpy package in the environments, we need to use the pip tool to install the numpy package.
        2. There are three types of subtasks, the first is a task that requires the use of APIs to access internet resources to obtain information, such as retrieving information from the Internet, this type of task is called 'API subtask', and the second is a task that does not require the use of API tools but need to write code to complete, which is called 'Code subtask', 'Code subtask' usually only involves operating system or file operations. The third is called 'QA subtask', It neither requires writing code nor calling API to complete the task, it will analyze the current subtask description and the return results of the predecessor tasks to get an appropriate answer.
        3. Each decomposed subtask has four attributes: name, task description, and dependencies. 'name' abstracts an appropriate name based on the reasoning process of the current subtask. 'description' is the process of the current subtask. 'dependencies' refers to the list of task names that the current task depends on based on the reasoning process. These tasks must be executed before the current task. 'type' indicates whether the current task is a Code task or a API task or a QA task, If it is a Code task, its value is 'Code', if it is a API task, its value is 'API', if it is a QA task, its value is 'QA'.
        4. Continuing with the example in 1, the format of the JSON data I want to get is as follows:
        ```json
        {
            "install_package" : {
                "name": "install_package",
                "description": "Use pip to install the numpy package that is missing in the environments.",
                "dependencies": [],
                "type" : "Code"
            }
        }
        ```
        And you should also follow the following criteria:
        1. The tasks you design based on the reasoning process are all atomic operations. You may need to design more than one task to meet the requirement that each task is an atomic operation.
        2. The Tool List I gave you contains the name of each tool and the corresponding operation description. These tools are all atomic operations. You can refer to these atomic operations to design new task.
        3. If an atomic operation in the Tool List can be used as a new task,  then the name of the decomposed sub-task should be directly adopted from the name of that atomic tool.
        4. The dependency relationship between the newly added task and the current task cannot form a loop.
        5. The description information of the new task must be detailed enough, no entity and operation information in the task can be ignored.
        6. 'Current Working Directiory' and 'Files And Folders in Current Working Directiory' specify the path and directory of the current working directory. These information may help you understand and generate tasks.
        7. The tasks currently designed are compatible with and can be executed on the present version of the system.
        8. Please note that the name of a task must be abstract. For instance, if the task is to search for the word "agents," then the task name should be "search_word," not "search_agent." As another example, if the task involves moving a file named "test," then the task name should be "move_file," not "move_test.
        9. Please note that QA subtasks will not be generated continuously, that is, there will be no dependency between any two QA subtasks.
        10. A QA subtask can perform comprehension analysis task, such as content conversion and format transformation, information summarization or analysis, answering academic questions, language translation, creative writing, logical reasoning based on existing information, and providing daily life advice and guidance, etc.
        ''',
        '_USER_TASK_REPLAN_PROMPT': '''
        User's information are as follows:
        Current Task: {current_task}
        Current Task Description: {current_task_description}
        System Version: {system_version}
        reasoning: {reasoning}
        Tool List: {tool_list}
        Current Working Directiory: {working_dir}
        Files And Folders in Current Working Directiory: {files_and_folders}
        ''',
    },

    'retrieve_prompt': {
        # tool code filter prompts
        '_SYSTEM_ACTION_CODE_FILTER_PROMPT': '''
        You are an expert in analyzing python code.
        I will assign you a task and provide a dictionary of tool names along with their corresponding codes. Based on the current task, please analyze the dictionary to determine if there is any tool whose code can be used to complete the task. If such a code exists, return the tool name that corresponds to the code you believe is best suited for completing the task. If no appropriate code exists, return an empty string.
        You should only respond with the format as described below:
        1. First, understand the requirements of the task. Next, read the code for each tool, understanding their functions and methods. Examine the methods and attributes within the class, learning about their individual purposes and return values. Finally, by combining the task with the parameters of each tool class's __call__ method, determine whether the content of the task can serve as an argument for the __call__ method, thereby arriving at an analysis result.
        2. Based on the above analysis results, determine whether there is code corresponding to the tool that can complete the current task. If so, return the tool name corresponding to the code you think is the most appropriate. If not, return an empty string.
        3. Output Format: The final output should include one part: the name of the selected tool or empty string, which must be enclosed in <action></action> tags.    
        And you should also follow the following criteria:
        1. There may be multiple codes that meet the needs of completing the task, but I only need you to return the tool name corresponding to the most appropriate code.
        2. If no code can complete the task, be sure to return an empty string, rather than a name of a tool corresponding to a code that is nearly but not exactly suitable.
        ''',
        '_USER_ACTION_CODE_FILTER_PROMPT': '''
        User's information are as follows:
        Tool Code Pair: {tool_code_pair}
        Task: {task_description}
        ''',
    },
    
    'self_learning_prompt' : {
        # self learning prompt
        '_SYSTEM_COURSE_DESIGN_PROMPT' : '''
        You are an expert in designing a python course focused entirely on using a specific Python package to operate a particular software, each lesson in the course includes specific tasks for operating the software package, as well as prompts for program input and output. Students will write Python code based on the content of each lesson and the relevant prompts to complete tasks, thereby learning how to use specific package to operate software.
        I will provide you with the name of the software you need to learn, the specific Python package required to operate it, and an example of course design. Additionally, there may be a provision of the software's demo file path and its contents. I want you to design a software learning course, aimed at mastering skills for performing specific software operations using specific python package. Please generate a progressively challenging course based on the information and criteria below.
        Excel Course Design Example: To help you better design a course on related software, here I provide you with an example of a course design for learning to manipulate Excel files using openpyxl. Lesson 1, use openpyxl to read all the contents of sheet 'Sheet1' in demo.xlsx, the input is the path of file and the name of the sheet, the output is the contents of 'Sheet1' in 'demo.xlsx' as a list of rows, where each row contains the data from the respective row in the sheet, and demo.xlsx is located in 'working_dir/demo.xlsx'. Lesson 2, use the Python package 'openpyxl' to read all the contents of column 'Product' of sheet 'Sheet1' in demo.xlsx, the input is the path of file, sheet name and column name, the output is the contents of column 'Product' of 'Sheet1' in 'demo.xlsx' as a list, and demo.xlsx is located in 'working_dir/demo.xlsx'. Lesson 3, use openpyxl to insert a new sheet named 'new sheet' into demo.xlsx, the input is the path of file and the name of the new sheet, the output is None, and demo.xlsx is located in 'working_dir/demo.xlsx'. Lesson 3, use the Python package 'openpyxl' to copy the 'Product' column from 'Sheet1' to 'Sheet2' in demo.xlsx. input is the path of the file, sheet name1, sheet name2, column name, output is None, and demo.xlsx is located in 'working_dir/demo.xlsx'. Lesson 5, use the Python package 'openpyxl' to create a histogram that represents the data from the 'Product' and 'Sales' columns in the 'Sheet1' of demo.xlsx, the input is the path of the file, sheet name, column name1, colunm name2, the output is None, and demo.xlsx is located in 'working_dir/demo.xlsx'. lesson 6, use openpyxl to sum the values under the 'sales' column from the sheet 'Sheet1', the input is the path of the file ,sheet name and column name, the output is the sum of the 'sales' column, and demo.xlsx is located in 'working_dir/demo.xlsx'. 
        Note that only six lessons are listed here for demonstration purposes; you will need to design the course to include as many lessons as possible to comprehensively learn Python package manipulation in practice.
        You should only respond with the format as described below:
        1. Output Format: The course designed consists of lessons, all lessons designed must be organised into a JSON data format, where key is the name of the lesson and value is a detailed description of the lesson.
        2. Course design: The design of the course must progress from easy to difficult, with the more complex and challenging lessons later in the course incorporating the objectives of the earlier lessons.
        3. lesson's name and description: The lesson's name is a summary of its current contents, and the description of the lesson have three or four parts: Task, Input, Output, File Path(If it exists). Task is a detailed description of the course content, Input is the prompt for the input of the program, Output is the prompt for the output of the program, and File Path is the path of the corresponding operating file. 
        4. Continuing with the Excel Course Design Example, the format of the JSON data I want to get is as follows:
        ```json
        {
            "read_specified_sheet" : "Task: Use the Python package 'openpyxl' to read all the contents of sheet 'Sheet1' in demo.xlsx. Input: The path of file, sheet name. Output: return the contents of 'Sheet1' in 'demo.xlsx' as a list of rows, where each row contains the data from the respective row in the sheet. File Path: working_dir/demo.xlsx",
            "read_specified_sheet_column" : "Task: Use the Python package 'openpyxl' to read all the contents of column 'Product' of sheet 'Sheet1' in demo.xlsx. Input: The path of file, sheet name and column name. Output: return the contents of column 'Product' of 'Sheet1' in 'demo.xlsx' as a list. File Path: working_dir/demo.xlsx",        
            "insert_new_sheet" : "Task: Use the Python package 'openpyxl' to insert a new sheet named 'new sheet' into demo.xlsx. Input: The path of file and the name of the new sheet. Output: None. File Path: working_dir/demo.xlsx",
            "copy_column_to_another_sheet" : "Task: Use the Python package 'openpyxl' to copy the 'Product' column from 'Sheet1' to 'Sheet2' in demo.xlsx. Input: The path of the file, sheet name1, sheet name2, column name. Output: None. File Path: working_dir/demo.xlsx",
            "plot_histogram_from_sheet " : "Task: Use the Python package 'openpyxl' to create a histogram that represents the data from the 'Product' and 'Sales' columns in the 'Sheet1' of demo.xlsx. Input: The path of the file, sheet name, column name1, colunm name2. Output: None. File Path: working_dir/demo.xlsx",
            "sum_column_values_in_sheet" : "Task: Use the Python package 'openpyxl' to sum the values under the 'Sales' column from the sheet 'Sheet1'. Input: The path of the file ,sheet name and column name. Output: The sum of the 'sales' column in 'Sheet1'. File Path: working_dir/demo.xlsx"
        }
        ```
        And you should also follow the following criteria:
        1. My goal is to learn and master all the functionalities of this package for operating the software, enabling practical solutions to real-world problems. Therefore, the course design should encompass all features of the package as comprehensively as possible.
        2. Each lesson's description should include the path of the corresponding operating file, if such a file exists, to facilitate learning directly on that file.
        3. Your operation is executed under the specified System Version, so you need to be aware that the generated course can be executed under that OS environment.
        4. If the Demo File Path is empty, you will need to generate a appropriate course, based on your understanding of the provided software and the package.
        5. If Demo File Path is not empty, you must have an in-depth understanding and analysis of File Content and design a comprehensive and detailed course based on File Content. 
        6. Please note, an output of 'None' means that when students are learning a lesson, the code they write does not need to return a value. They only need to write the code according to the lesson task and input prompts to perform operations on the file.
        7. To help students better learn the course and achieve the teaching objectives, the tasks in the lessons must be as detailed and unambiguous as possible.
        8. The code written by students during their course must be sufficiently versatile. Therefore, when designing the course, you should be able to transform the key information of tasks within the lesson into function parameters. Moreover, each parameter's content should be explicitly detailed in the Input and Output sections.
        ''',
        '_USER_COURSE_DESIGN_PROMPT' : '''
        User's information are as follows:
        Software Name: {software_name}
        Python Package Name: {package_name}
        Demo File Path: {demo_file_path} 
        File Content: {file_content}
        System Version: {system_version}
        ''',       

    },

    'text_extract_prompt' : '''
        Please return all the contents of the file. 
        File Path: {file_path}
        Tips: 
        1. You need to be aware that the contents of some files may be stored in different places, for example, the contents of Excel may stored in different sheets and the contents of PPT may stored in different slides. For such files, I would like to return the contents of files in a dictionary format, organized by each sheet or slide, for easy retrieval and reading.
        2. You can only break down the task into one subtask. The subtask is for reading out all the contents of the file.
        3. If the file is a sheet file, I would like the output to be a dictionary, the key should be the name of each sheet, and the value should be a list of lists, where each inner list contains the contents of a row from that sheet.
        '''
    
}
