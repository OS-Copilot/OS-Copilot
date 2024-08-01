LightFriday: A Lightweight Agent for Task Execution
========================================================================

In this tutorial, we will explore how to use the ``LightFriday`` class, a lightweight agent designed to autonomously execute code and complete tasks. We will walk through the core components and functionality of ``LightFriday``, demonstrating how it leverages code execution and iterative planning to achieve task completion.

Task Overview
----------------

We will undertake a specific task, **"Plot AAPL and META's normalized stock prices,"** using the ``LightFriday`` agent. The agent will execute code step-by-step to complete this task.

Initial Setup
----------------

1. **Setting Up the Configuration**:

    Before we initialize the ``LightFriday`` agent, we need to set up the configuration. This involves setting up the system environment and loading the task details.

    .. code-block:: python

        from oscopilot.utils import setup_config, setup_pre_run

        args = setup_config()
        if not args.query:
            args.query = "Plot AAPL and META's normalized stock prices"
        task = setup_pre_run(args)

Core Component: ``LightFriday``
-------------------------------

The ``LightFriday`` class is the core component of this tutorial. It inherits from the ``BaseModule`` class and is responsible for planning, executing code, and iterating until the task is complete.

1. **Initialization**:

The ``LightFriday`` class is initialized with the following parameters:

.. code-block:: python

    class LightFriday(BaseModule):
        def __init__(self, args):
            super().__init__()
            self.args = args

2. **Execution Tool**:

The ``execute_tool`` method executes the given code in the specified language and returns the execution result or error.

.. code-block:: python

    def execute_tool(self, code, lang):
        state = self.environment.step(lang, code)
        return_info = ''
        if state.result != None and state.result.strip() != '':
            return_info = '**Execution Result** :' + state.result.strip()
        if state.error != None and state.error.strip() != '':
            return_info = '\n**Execution Error** :' + state.error.strip()
        return return_info.strip()

3. **Main Functionality**:

The ``run`` method is the heart of the ``LightFriday`` agent. It involves the following steps:

- **System Prompt**: Defines the system prompt with instructions for ``LightFriday``.

    .. code-block:: python

        light_planner_sys_prompt = '''You are Light Friday, a world-class programmer that can complete any goal by executing code...
        '''

- **User Prompt**: Provides details about the user's system and the task to be completed.

    .. code-block:: python

        light_planner_user_prompt = '''
        User's information are as follows:
        System Version: {system_version}
        Task: {task}
        Current Working Directiory: {working_dir}'''.format(system_version=self.system_version, task=task, working_dir=self.environment.working_dir)

- **Message Loop**: Iteratively interacts with the language model, executing code and refining the plan based on the results.

    .. code-block:: python

        message = [
            {"role": "system", "content": light_planner_sys_prompt},
            {"role": "user", "content": light_planner_user_prompt},
        ]

        while True:
            response = send_chat_prompts(message, self.llm)
            rich_print(response)
            message.append({"role": "system", "content": response})

            code, lang = extract_code(response)
            if code:
                result = self.execute_tool(code, lang)
                rich_print(result)
            else:
                result = ''

            if result != '':
                light_exec_user_prompt = 'The result after executing the code: {result}'.format(result=result)
                message.append({"role": "user", "content": light_exec_user_prompt})
            else:
                message.append({"role": "user", "content": "Please continue. If all tasks have been completed, reply with 'Execution Complete'. If you believe subsequent tasks cannot continue, reply with 'Execution Interrupted', including the reasons why the tasks cannot proceed, and provide the user with some possible solutions."})

            if 'Execution Complete' in response or 'Execution Interrupted' in response:
                break

Running the Task
----------------

To run the task using ``LightFriday``, we initialize the agent and call the ``run`` method with the task details:

.. code-block:: python

    light_friday = LightFriday(args)
    light_friday.run(task)

Conclusion
--------------

This tutorial demonstrated how to use the ``LightFriday`` class to execute tasks by iteratively planning and executing code. By leveraging the ``LightFriday`` agent, complex tasks can be broken down into manageable steps, and code can be executed step-by-step to achieve the desired outcomes.

This process showcases ``LightFriday``'s capability to adapt and evolve, making it a powerful tool for automating a wide range of tasks.