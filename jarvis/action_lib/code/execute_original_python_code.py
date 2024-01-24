from jarvis.action.base_action import BaseAction
import subprocess
import os
import sys
import tempfile

class execute_original_python_code(BaseAction):
    def __init__(self):
        self._description = "Execute the Python code read from a file and get the original output."

    def __call__(self, python_code, working_dir=None, *args, **kwargs):
        """
        Execute the provided Python code and print the output.

        Args:
            python_code (str): The Python code to be executed.
            working_dir (str, optional): The working directory where the code should be executed. Defaults to the current working directory.

        Returns:
            The result of the Code execution.
        """
        # Set the working directory if provided, otherwise use the current working directory
        if working_dir:
            os.chdir(working_dir)
        else:
            working_dir = os.getcwd()

        # Create a temporary file to store the Python code
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.py', dir=working_dir, delete=False) as temp_file:
            temp_file_name = temp_file.name
            temp_file.write(python_code)
            temp_file.flush()

            # Execute the Python code using the Python interpreter
            try:
                result = subprocess.run([sys.executable, temp_file_name], capture_output=True, text=True, check=True)
                return result.stdout.strip()
            except subprocess.CalledProcessError as e:
                print(f"An error occurred while executing the Python code: {e.stderr}", file=sys.stderr)
            finally:
                # Remove the temporary file
                os.unlink(temp_file_name)

# Example of how to use the class (this should be in the comments):
# executor = execute_original_python_code()
# executor(python_code=read_python_code_return_val[0], working_dir='/home/heroding/桌面/Jarvis/working_dir')