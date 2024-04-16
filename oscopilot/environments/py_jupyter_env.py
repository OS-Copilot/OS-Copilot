# This code is based on Open Interpreter. Original source: https://github.com/OpenInterpreter/open-interpreter

import ast
import os
import sys
import queue
import re
import threading
import time
import traceback
import logging

from jupyter_client import KernelManager
from oscopilot.environments.base_env import BaseEnv


# turn off colors in "terminal"
# os.environ["ANSI_COLORS_DISABLED"] = "1"


class PythonJupyterEnv(BaseEnv):
    """
    A class representing an environment for executing Python code in a Jupyter environment.

    This class manages the execution of Python code using IPython kernel, providing methods for preprocessing code,
    executing code steps, handling output messages, and terminating the kernel.

    It inherits from BaseEnv, which provides basic environment functionality.
    """    
    file_extension = "py"
    name = "Python"
    aliases = ["py", "API"]

    def __init__(self):
        """
        Initializes the Python Jupyter environment.

        This method sets up the IPython kernel manager and client, starts the kernel, and configures logging.
        """        
        super().__init__()
        ipkernel_logger = logging.getLogger('IPKernelApp')

        # Create a filter using a lambda function
        warning_filter = lambda record: not any(msg in record.getMessage() for msg in [
            "Parent appears to have exited, shutting down.",
            "Could not destroy zmq context"
        ])
        # Add the filter to the logger
        ipkernel_logger.addFilter(warning_filter)

        # Get the path to the current Python executable
        python_executable = sys.executable
        
        # Ensure only one KernelManager instance is configured and started
        self.km = KernelManager(kernel_name='python3', kernel_cmd=[python_executable, '-m', 'ipykernel_launcher', '-f', '{connection_file}'])
        self.km.start_kernel(env=os.environ.copy())
        # self.km.start_kernel()
        self.kc = self.km.client()
        self.kc.start_channels()
        while not self.kc.is_alive():
            time.sleep(0.1)
        time.sleep(0.5)
        '''
        ipkernel_logger = logging.getLogger('IPKernelApp')
        # Create a filter using a lambda function
        warning_filter = lambda record: not any(msg in record.getMessage() for msg in [
            "Parent appears to have exited, shutting down.",
            "Could not destroy zmq context"
        ])
        # Add the filter to the logger
        ipkernel_logger.addFilter(warning_filter)

        # Get the path to the current Python executable
        python_executable = sys.executable
        
        # Create a KernelManager instance using the current Python executable
        self.km = KernelManager(kernel_name='python3', kernel_cmd=[python_executable, '-m', 'ipykernel_launcher', '-f', '{connection_file}'])
        # self.km.start_kernel()
        # self.kc = self.km.client()
        # self.kc.start_channels()
            
        # self.km = KernelManager(kernel_name="python3")
        self.km.start_kernel()
        self.kc = self.km.client()
        self.kc.start_channels()
        while not self.kc.is_alive():
            time.sleep(0.1)
        time.sleep(0.5)
        '''
        self.listener_thread = None
        self.finish_flag = False

        # DISABLED because sometimes this bypasses sending it up to us for some reason!
        # Give it our same matplotlib backend
        # backend = matplotlib.get_backend()

#         # Use Agg, which bubbles everything up as an image.
#         # Not perfect (I want interactive!) but it works.
#         backend = "Agg"

#         code = f"""
# import matplotlib
# matplotlib.use('{backend}')
#         """.strip()
#         for _ in self.run(code):
#             pass

        # DISABLED because it doesn't work??
        # Disable color outputs in the terminal, which don't look good in OI and aren't useful
        # code = """
        # from IPython.core.getipython import get_ipython
        # get_ipython().colors = 'NoColor'
        # """
        # self.run(code)

    def terminate(self):
        """
        Terminates the IPython kernel and stops its channels.
        """
        self.kc.stop_channels()
        self.km.shutdown_kernel()

    def step(self, code):
        """
        Executes a step of Python code.

        Args:
            code (str): The Python code to execute.

        Yields:
            dict: Output messages generated during execution.
        """        
        # 解析python代码并且将函数体抽取出来存成字典，key是函数名，value是函数体，如果要存的话，就将每个函数存成一个py文件
        # try:
        #     functions = string_to_python(code)  # 
        # except:
        #     # Non blocking
        #     functions = {}

        # if self.computer.save_skills and functions:
        #     skill_library_path = self.computer.skills.path

        #     if not os.path.exists(skill_library_path):
        #         os.makedirs(skill_library_path)

        #     for filename, function_code in functions.items():
        #         with open(f"{skill_library_path}/{filename}.py", "w") as file:
        #             file.write(function_code)

        self.finish_flag = False
        try:
            try:
                preprocessed_code = self.preprocess_code(code)
            except:
                # Any errors produced here are our fault.
                # Also, for python, you don't need them! It's just for active_line and stuff. Just looks pretty.
                preprocessed_code = code
            message_queue = queue.Queue()
            self._execute_code(preprocessed_code, message_queue)
            yield from self._capture_output(message_queue)
        except GeneratorExit:
            raise  # gotta pass this up!
        except:
            content = traceback.format_exc()
            yield {"type": "console", "format": "output", "content": content}

    def _execute_code(self, code, message_queue):
        """
        Executes Python code using the IPython kernel and captures the output messages.

        Args:
            code (str): The Python code to execute.
            message_queue (queue.Queue): The message queue for storing output messages.
        """        
        def iopub_message_listener():
            '''
            The main function of this function is to monitor the messages on the IOPub message channel of the IPython kernel and 
            process them accordingly according to the type of the message. The IOPub message channel is a channel in the Jupyter/IPython 
            system used to broadcast execution results, logs, errors, status updates and other information.            
            '''
            while True:
                # If self.finish_flag = True, and we didn't set it (we do below), we need to stop. That's our "stop"
                if self.finish_flag == True:
                    self.km.interrupt_kernel()
                    return
                try:
                    msg = self.kc.iopub_channel.get_msg(timeout=0.05)
                except queue.Empty:
                    continue

                if (
                    msg["header"]["msg_type"] == "status"
                    and msg["content"]["execution_state"] == "idle"
                ):
                    # Set finish_flag and return when the kernel becomes idle

                    self.finish_flag = True
                    return

                content = msg["content"]

                if msg["msg_type"] == "stream":
                    line, active_line = self.detect_active_line(content["text"])
                    if active_line:
                        message_queue.put(
                            {
                                "type": "console",
                                "format": "active_line",
                                "content": active_line,
                            }
                        )
                    message_queue.put(
                        {"type": "console", "format": "output", "content": line}
                    )
                elif msg["msg_type"] == "error":
                    content = "\n".join(content["traceback"])
                    # Remove color codes
                    ansi_escape = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")
                    content = ansi_escape.sub("", content)
                    message_queue.put(
                        {
                            "type": "console",
                            "format": "output",
                            "content": content,
                        }
                    )
                elif msg["msg_type"] in ["display_data", "execute_result"]:
                    data = content["data"]
                    if "image/png" in data:
                        message_queue.put(
                            {
                                "type": "image",
                                "format": "base64.png",
                                "content": data["image/png"],
                            }
                        )
                    elif "image/jpeg" in data:
                        message_queue.put(
                            {
                                "type": "image",
                                "format": "base64.jpeg",
                                "content": data["image/jpeg"],
                            }
                        )
                    elif "text/html" in data:
                        message_queue.put(
                            {
                                "type": "code",
                                "format": "html",
                                "content": data["text/html"],
                            }
                        )
                    elif "text/plain" in data:
                        message_queue.put(
                            {
                                "type": "console",
                                "format": "output",
                                "content": data["text/plain"],
                            }
                        )
                    elif "application/javascript" in data:
                        message_queue.put(
                            {
                                "type": "code",
                                "format": "javascript",
                                "content": data["application/javascript"],
                            }
                        )

        self.listener_thread = threading.Thread(target=iopub_message_listener)
        # self.listener_thread.daemon = True
        self.listener_thread.start()

        self.kc.execute(code)

    def detect_active_line(self, line):
        """
        Detects active line markers in the output line.

        Args:
            line (str): The output line from the IPython kernel.

        Returns:
            tuple: The modified line and active line number, if detected.
        """        
        if "##active_line" in line:
            # Split the line by "##active_line" and grab the last element
            last_active_line = line.split("##active_line")[-1]
            # Split the last active line by "##" and grab the first element
            active_line = int(last_active_line.split("##")[0])
            # Remove all ##active_line{number}##\n
            line = re.sub(r"##active_line\d+##\n", "", line)
            return line, active_line
        return line, None

    def _capture_output(self, message_queue):
        """
        Captures output messages from the message queue.

        Args:
            message_queue (queue.Queue): The message queue.

        Yields:
            dict: Output messages.
        """        
        while True:
            if self.listener_thread:
                try:
                    output = message_queue.get(timeout=0.1)
                    yield output
                except queue.Empty:
                    if self.finish_flag:
                        break
            time.sleep(0.1)

    def stop(self):
        """
        Stops the execution of code by setting the finish flag.
        """        
        self.finish_flag = True

    def preprocess_code(self, code):
        """
        Preprocesses the Python code before execution.

        Args:
            code (str): The Python code to preprocess.

        Returns:
            str: The preprocessed code.
        """
        code = code.strip()

        # Add print commands that tell us what the active line is
        # but don't do this if any line starts with ! or %
        if not any(line.strip().startswith(("!", "%")) for line in code.split("\n")):
            code = add_active_line_prints(code)

        # Wrap in a try except (DISABLED)
        # code = wrap_in_try_except(code)

        # Remove any whitespace lines, as this will break indented blocks
        # (are we sure about this? test this)
        code_lines = code.split("\n")
        code_lines = [c for c in code_lines if c.strip() != ""]
        code = "\n".join(code_lines)

        return code
    

def add_active_line_prints(code):
    """
    Adds print statements indicating line numbers to a Python string.

    Args:
        code (str): The Python code.

    Returns:
        str: The code with added print statements.
    """
    # Replace newlines and comments with pass statements, so the line numbers are accurate (ast will remove them otherwise)
    code_lines = code.split("\n")
    in_multiline_string = False
    for i in range(len(code_lines)):
        line = code_lines[i]
        if '"""' in line or "'''" in line:
            in_multiline_string = not in_multiline_string
        if not in_multiline_string and (line.strip().startswith("#") or line == ""):
            whitespace = len(line) - len(line.lstrip(" "))
            code_lines[i] = " " * whitespace + "pass"
    processed_code = "\n".join(code_lines)
    try:
        tree = ast.parse(processed_code)
    except:
        # If you can't parse the processed version, try the unprocessed version before giving up
        tree = ast.parse(code)
    transformer = AddLinePrints()
    new_tree = transformer.visit(tree)
    return ast.unparse(new_tree)


class AddLinePrints(ast.NodeTransformer):
    """
    Transformer to insert print statements indicating the line number
    before every executable line in the AST.
    """

    def insert_print_statement(self, line_number):
        """
        Inserts a print statement for a given line number.

        Args:
            line_number (int): The line number.

        Returns:
            ast.Expr: The print statement AST node.
        """
        return ast.Expr(
            value=ast.Call(
                func=ast.Name(id="print", ctx=ast.Load()),
                args=[ast.Constant(value=f"##active_line{line_number}##")],
                keywords=[],
            )
        )

    def process_body(self, body):
        """
        Processes a block of statements, adding print calls.

        Args:
            body (list): List of AST nodes representing statements.

        Returns:
            list: List of modified AST nodes.
        """
        new_body = []

        # In case it's not iterable:
        if not isinstance(body, list):
            body = [body]

        for sub_node in body:
            if hasattr(sub_node, "lineno"):
                new_body.append(self.insert_print_statement(sub_node.lineno))
            new_body.append(sub_node)

        return new_body

    def visit(self, node):
        """
        Visits and transforms nodes in the AST.

        Args:
            node: The current AST node.

        Returns:
            ast.Node: The modified AST node.
        """
        new_node = super().visit(node)

        # If node has a body, process it
        if hasattr(new_node, "body"):
            new_node.body = self.process_body(new_node.body)

        # If node has an orelse block (like in for, while, if), process it
        if hasattr(new_node, "orelse") and new_node.orelse:
            new_node.orelse = self.process_body(new_node.orelse)

        # Special case for Try nodes as they have multiple blocks
        if isinstance(new_node, ast.Try):
            for handler in new_node.handlers:
                handler.body = self.process_body(handler.body)
            if new_node.finalbody:
                new_node.finalbody = self.process_body(new_node.finalbody)

        return new_node


def wrap_in_try_except(code):
    """
    Wraps Python code in a try-except block to catch exceptions.

    Args:
        code (str): The Python code.

    Returns:
        str: The code wrapped in a try-except block.
    """
    code = "import traceback\n" + code

    # Parse the input code into an AST
    parsed_code = ast.parse(code)

    # Wrap the entire code's AST in a single try-except block
    try_except = ast.Try(
        body=parsed_code.body,
        handlers=[
            ast.ExceptHandler(
                type=ast.Name(id="Exception", ctx=ast.Load()),
                name=None,
                body=[
                    ast.Expr(
                        value=ast.Call(
                            func=ast.Attribute(
                                value=ast.Name(id="traceback", ctx=ast.Load()),
                                attr="print_exc",
                                ctx=ast.Load(),
                            ),
                            args=[],
                            keywords=[],
                        )
                    ),
                ],
            )
        ],
        orelse=[],
        finalbody=[],
    )

    # Assign the try-except block as the new body
    parsed_code.body = [try_except]

    # Convert the modified AST back to source code
    return ast.unparse(parsed_code)


def string_to_python(code_as_string):
    """
    Parses Python code from a string and extracts function definitions.

    Args:
        code_as_string (str): The Python code as a string.

    Returns:
        dict: A dictionary mapping function names to their code.
    """    
    parsed_code = ast.parse(code_as_string)

    # Initialize containers for different categories
    import_statements = []
    functions = []
    functions_dict = {}

    # Traverse the AST
    for node in ast.walk(parsed_code):
        # Check for import statements
        if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
            for alias in node.names:
                # Handling the alias in import statements
                if alias.asname:
                    import_statements.append(f"import {alias.name} as {alias.asname}")
                else:
                    import_statements.append(f"import {alias.name}")
        # Check for function definitions
        elif isinstance(node, ast.FunctionDef):
            if node.name.startswith("_"):
                # ignore private functions
                continue
            docstring = ast.get_docstring(node)
            body = node.body
            if docstring:
                body = body[1:]

            code_body = ast.unparse(body[0]).replace("\n", "\n    ")

            func_info = {
                "name": node.name,
                "docstring": docstring,
                "body": code_body,
            }
            functions.append(func_info)

    for func in functions:
        # Consolidating import statements and function definition
        function_content = "\n".join(import_statements) + "\n\n"
        function_content += f"def {func['name']}():\n    \"\"\"{func['docstring']}\"\"\"\n    {func['body']}\n"

        # Adding to dictionary
        functions_dict[func["name"]] = function_content

    return functions_dict


def main():
    env = PythonJupyterEnv()
    code = '''from oscopilot.tool_repository.basic_tools.base_action import BaseAction
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
create_folder_action = create_folder()
create_folder_action(working_directory='/Users/hanchengcheng/Documents/official_space/os-copilot-private/working_dir', folder_name='my_new_folder')
'''
    for _ in env.run(code):
        print(_)

if __name__ == '__main__':
    main()