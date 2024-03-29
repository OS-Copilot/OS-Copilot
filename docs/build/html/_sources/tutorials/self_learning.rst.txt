Enhancing FRIDAY with Self-Learning for Excel Task Automation
========================================================================

In this tutorial, we will explore how FRIDAY's self-learning feature enables it to autonomously learn and execute tasks involving Excel file manipulation, which were initially beyond its capability. We will specifically focus on a task from the SheetCopilot dataset and observe how FRIDAY evolves to complete it successfully using the `openpyxl` library.

Task Overview
----------------

You will undertake a specific task (task #9) from the SheetCopilot dataset,
which involves manipulating an Excel file. 
The task is **"Copy the 'Product' column from 'Sheet1' to a new sheet named 'Sheet2', and then sort the 'Product' column in 'Sheet2' in ascending order."**

Initial Attempt
-----------------

1. **Running the Task**:

    Execute the following command in your terminal to run task #9 from the SheetCopilot dataset:

    .. code-block:: shell

        python examples/SheetCopilot/run_sheet_task.py --sheet_task_id 9

    The `run_sheet_task.py` script serves as the interface for FRIDAY to interact with tasks defined in the SheetCopilot dataset. Below is a brief explanation of the script's content:

    - Module Imports and Configuration Setup:

        .. code-block:: python

            from oscopilot import FridayAgent
            from oscopilot import FridayExecutor, FridayPlanner, FridayRetriever, ToolManager
            from oscopilot.utils import setup_config, SheetTaskLoader

    - Loading Tasks:

        The script initializes the configuration and loads the task based on the provided task ID using SheetTaskLoader.

        .. code-block:: python

            args = setup_config()
            sheet_task_loader = SheetTaskLoader("examples/SheetCopilot/sheet_task.jsonl")

    - FRIDAY Agent Initialization:

        An agent is initialized with components such as the Planner, Retriever, Executor, and Tool Manager, configured with the loaded arguments.

        .. code-block:: python

            agent = FridayAgent(FridayPlanner, FridayRetriever, FridayExecutor, ToolManager, config=args)

    - Task Execution:

        If a specific task ID is provided, the script fetches and runs that task. Otherwise, it loads and executes each task in the dataset sequentially.

        .. code-block:: python

            if args.sheet_task_id:
                task = sheet_task_loader.get_data_by_task_id(args.sheet_task_id)
                agent.run(task)
            else:
                task_lst = sheet_task_loader.load_sheet_task_dataset()
                for task_id, task in enumerate(task_lst):
                args.sheet_task_id = task_id
                agent.run(task)

However, you'll notice that FRIDAY **is unable to** complete the task due to lacking specific tools for Excel manipulation.


Introducing Self-Learning
---------------------------

2. **Enabling FRIDAY to Learn**:

    To overcome this limitation, we introduce FRIDAY to a self-learning module that allows it to explore and learn from the `openpyxl` library, thereby acquiring new tools for Excel file operations.

    Run the self-learning command:

    .. code-block:: shell

        python course_learning.py --software_name Excel --package_name openpyxl --demo_file_path working_dir/Invoices.xlsx

    This command directs FRIDAY to learn how to manipulate Excel files using the `openpyxl` library. Below is a brief overview of the `course_learning.py` script's functionality:

    - Import Statements and Configuration Setup:

    .. code-block:: python

        from oscopilot import FridayAgent, FridayExecutor, FridayPlanner, FridayRetriever, SelfLearner, SelfLearning, ToolManager, TextExtractor
        from oscopilot.utils import setup_config

    - Initialization and Configuration Extraction:

    The script begins by setting up the configuration and extracting parameters for the software name, package name, and a demo file path.

    .. code-block:: python

        args = setup_config()
        software_name = args.software_name
        package_name = args.package_name
        demo_file_path = args.demo_file_path

    - FRIDAY Agent and Self-Learning Module Initialization:

    A FRIDAY agent is initialized with components such as the Planner, Retriever, Executor, and Tool Manager. The SelfLearning module is then initialized with the agent, allowing it to engage in self-learning activities.

    .. code-block:: python

        friday_agent = FridayAgent(FridayPlanner, FridayRetriever, FridayExecutor, ToolManager, config=args)
        self_learning = SelfLearning(friday_agent, SelfLearner, ToolManager, args, TextExtractor)

    - Self-Learning Process:

    The SelfLearning module embarks on exploring the openpyxl library, utilizing the provided demo file as a learning resource.

    .. code-block:: python

        self_learning.self_learning(software_name, package_name, demo_file_path)

Through this exploratory process, FRIDAY can learn various tools such as `check_openpyxl_installed`, `read_excel_contents`, `filter_product_data`, and `export_filtered_data`, among others.

.. note::

     The tools learned through self-learning have a degree of randomness.


Verifying the Learning Outcome
--------------------------------

3. **Re-running the Task**:

    After the self-learning process, rerun the initial task to verify the effectiveness of the self-learning module:

    .. code-block:: shell

        python examples/SheetCopilot/run_sheet_task.py --sheet_task_id 9

    This time, FRIDAY will successfully complete the task, demonstrating the acquired ability to manipulate Excel files through the learned tools.


Conclusion
--------------

This tutorial showcased the innovative self-learning feature of FRIDAY, which enables it to autonomously expand its toolset and adapt to tasks it was initially unable to perform. 
By engaging in self-learning with the `openpyxl` library, FRIDAY demonstrated a significant improvement in handling Excel file operations, affirming the effectiveness and potential of self-learning in AI agents.

This process highlights FRIDAY's capability to evolve and adapt, making it a powerful tool for automating a wide range of tasks, including complex file manipulations.