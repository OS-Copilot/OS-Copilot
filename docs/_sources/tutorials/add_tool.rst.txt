Adding Your Tools
=================================================

This tutorial will guide you through the process of adding a new tool to the FRIDAY platform. We will use a simple example tool, `create_folder.py`, to demonstrate the process.

Step 1: Clone the Repository
----------------------------

First, you need to clone the repository containing the tools (referred to as "gizmos" for FRIDAY). Use the following command to clone the repository:

.. code-block:: shell

   git clone https://github.com/OS-Copilot/FRIDAY-Gizmos.git

After cloning, navigate into the `FRIDAY-Gizmos` directory:

.. code-block:: shell

   cd FRIDAY-Gizmos

Choose any Python file that represents the tool code you wish to add. For this tutorial, we will use `Basic/create_folder.py` as an example.

Step 2: Add the Tool to FRIDAY
------------------------------

To add your chosen tool to FRIDAY's tool repository, run the `action_manager.py` script with the `--add` flag. You will need to provide the tool name and the path to the tool. Replace `[tool_name]` with the name you wish to give your tool and `[tool_path]` with the relative or absolute path to the tool file.

.. code-block:: shell

   python oscopilot/tool_repository/manager/tool_manager.py --add --tool_name [tool_name] --tool_path [tool_path]

.. note::
   
   - **[tool_name]:** A unique identifier for your tool within the FRIDAY ecosystem. It is recommended to keep the `tool_name` the same as the class name for consistency.
   - **[tool_path]:** The path to the Python file you're adding, relative to the FRIDAY installation directory or an absolute path.

Example: Adding a Tool
-----------------------

If we're adding the `create_folder.py` tool located in the `Basic` directory and we wish to name it `create_folder`, the command would look like this:

.. code-block:: shell

   python oscopilot/tool_repository/manager/tool_manager.py --add --tool_name create_folder --tool_path Basic/create_folder.py

Removing a Tool from FRIDAY
-----------------------------

In addition to adding new tools to FRIDAY, you might find yourself in a situation where you need to remove an existing tool from the tool repository. Whether it's for updating purposes or simply because the tool is no longer needed, removing a tool is straightforward.

To remove a tool from FRIDAY's tool repository, you can use the `action_manager.py` script with the `--delete` flag. You will need to specify the name of the tool you wish to remove using the `--tool_name` option. Replace `[tool_name]` with the unique identifier for your tool within the FRIDAY ecosystem.

.. code-block:: shell

   python oscopilot/tool_repository/manager/tool_manager.py --delete --tool_name [tool_name]

.. note::

   - **[tool_name]:** The unique identifier of the tool you want to remove from FRIDAY. Ensure that you provide the exact name as registered in FRIDAY's tool repository to avoid any errors.

Example: Removing a Tool
--------------------------

If you wish to remove a tool named `create_folder`, the command would look like this:

.. code-block:: shell

   python oscopilot/tool_repository/manager/tool_manager.py --delete --tool_name create_folder

This command will remove the `create_folder` tool from FRIDAY's repository, effectively making it unavailable for future use within the ecosystem. It's important to note that removing a tool is a permanent action, so make sure you've backed up any necessary code or information related to the tool before proceeding with the deletion.


Tool Code Example
------------------

To add a tool to FRIDAY, the tool code must follow a specific structure. Below is an example of a tool code that creates a folder either in a specified working directory or in the default working directory. This example adheres to the required structure for FRIDAY tools:

.. code-block:: python

   from oscopilot.tool_repository.basic_tools.base_action import BaseAction
   import os

   class create_folder(BaseAction):
       def __init__(self):
           self._description = "Create a folder under the default working directory."

       def __call__(self, working_directory=None, folder_name='myfold', *args, **kwargs):
           """
           Create a folder under the specified working directory or the default working directory.

           Args:
           working_directory (str): The path of the working directory. If not provided, the default working directory will be used.
           folder_name (str): The name of the folder to be created. Default is 'myfold'.

           Returns:
           None
           """
           # Check if the working_directory is provided, if not, use the default working directory
           if working_directory:
               os.chdir(working_directory)

           # Create the folder
           os.makedirs(folder_name)

   # Example of how to use the class
   # create_folder_action = create_folder()
   # create_folder_action(working_directory='/home/user/Desktop/FRIDAY/working_dir', folder_name='my_new_folder')

Tool Requirements
-----------------

To ensure seamless integration into FRIDAY's tool repository, your tool code must adhere to the following format, consistent with the example tools provided:

1. **BaseAction Inheritance**:
   Each tool must import and inherit from `BaseAction` provided by FRIDAY. Additionally, import any other necessary Python packages for your tool's functionality.

   .. code-block:: python

      from oscopilot.tool_repository.basic_tools.base_action import BaseAction
      import os  # Example of importing another necessary package

2. **Class Naming**:
   The name of the class should be consistent with the tool's file name to maintain clarity and ease of identification within the tool repository.

3. **Initialization Method**:
   The `__init__` method of your tool class must set `self._description`. This description should briefly outline the specific functionality of the tool, aiding in tool retrieval and user understanding.

   .. code-block:: python

      def __init__(self):
          self._description = "Description of what the tool does."

4. **Execution Method**:
   The `__call__` method is where the tool's specific execution code resides. It should include detailed explanations of the input and output parameters to guide the user.

   .. code-block:: python

      def __call__(self, parameter1, parameter2=None, *args, **kwargs):
          """
          Detailed explanation of what this method does, its parameters, and what it returns.
          """

5. **Usage Example**:
   At the end of your tool code, provide a usage example in the form of comments. This assists users and FRIDAY in understanding how to utilize the tool effectively. If the tool is automatically generated by FRIDAY, it will already meet these requirements.

   .. code-block:: python

      # Example of how to use the class
      # tool_instance = ClassName()
      # tool_instance(parameter1='value1', parameter2='value2')

By following these specific requirements, you ensure that your tool can be effectively integrated and utilized within the FRIDAY ecosystem. This consistency not only aids in tool management but also enhances the user experience by providing a standardized approach to tool development.


Conclusion
----------

With the provided guidelines and example, you are now equipped to extend FRIDAY's capabilities by adding new tools. By adhering to the structure and requirements specified for FRIDAY tools, you ensure that your tools can be effectively utilized within the FRIDAY ecosystem.

Remember, the power of FRIDAY lies in its flexibility and the collaborative efforts of its community. Your contributions help make FRIDAY more versatile and powerful. 

We welcome you to submit your tools to the FRIDAY Gizmos repository at https://github.com/OS-Copilot/FRIDAY-Gizmos. Sharing your work enables others in the community to benefit from your contributions and further enhances the FRIDAY platform.

Happy coding!
