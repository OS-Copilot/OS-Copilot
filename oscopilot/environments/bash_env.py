# This code is based on Open Interpreter. Original source: https://github.com/OpenInterpreter/open-interpreter

import os
import platform
import queue
import re
import subprocess
import threading
import time
import traceback
from oscopilot.environments import SubprocessEnv


class Shell(SubprocessEnv):
    """
    A class representing a shell environment for executing shell scripts.

    This class inherits from SubprocessEnv, which provides a general environment for executing code in subprocesses.
    """    
    file_extension = "sh"
    name = "Shell"
    aliases = ["bash", "sh", "zsh"]

    def __init__(
        self,
    ):
        """
        Initializes the Shell environment.

        Determines the start command based on the platform.
        """        
        super().__init__()

        # Determine the start command based on the platform
        if platform.system() == "Windows":
            self.start_cmd = ["cmd.exe"]
        else:
            self.start_cmd = [os.environ.get("SHELL", "bash")]

    def preprocess_code(self, code):
        """
        Preprocesses the shell script code before execution.

        Args:
            code (str): The shell script code to preprocess.

        Returns:
            str: The preprocessed shell script code.
        """        
        return preprocess_shell(code)

    def line_postprocessor(self, line):
        """
        Postprocesses each line of output from the shell execution.

        Args:
            line (str): A line from the output of the shell script execution.

        Returns:
            str: The processed line.
        """        
        return line

    def detect_active_line(self, line):
        """
        Detects the active line indicator in the output.

        Args:
            line (str): A line from the output.

        Returns:
            int: The line number indicated by the active line indicator, or None if not found.
        """        
        if "##active_line" in line:
            return int(line.split("##active_line")[1].split("##")[0])
        return None

    def detect_end_of_execution(self, line):
        """
        Detects the end of execution marker in the output.

        Args:
            line (str): A line from the output.

        Returns:
            bool: True if the end of execution marker is found, False otherwise.
        """        
        return "##end_of_execution##" in line


def preprocess_shell(code):
    """
    Preprocesses the shell script code before execution.

    Adds active line markers, wraps in a try-except block (trap in shell), and adds an end of execution marker.

    Args:
        code (str): The shell script code to preprocess.

    Returns:
        str: The preprocessed shell script code.
    """

    # Add commands that tell us what the active line is
    # if it's multiline, just skip this. soon we should make it work with multiline
    if not has_multiline_commands(code):
        code = add_active_line_prints(code)

    # Add end command (we'll be listening for this so we know when it ends)
    code += '\necho "##end_of_execution##"'

    return code


def add_active_line_prints(code):
    """
    Adds echo statements indicating line numbers to a shell script.

    Args:
        code (str): The shell script code to add active line indicators to.

    Returns:
        str: The modified shell script code with active line indicators.
    """
    lines = code.split("\n")
    for index, line in enumerate(lines):
        # Insert the echo command before the actual line
        lines[index] = f'echo "##active_line{index + 1}##"\n{line}'
    return "\n".join(lines)


def has_multiline_commands(script_text):
    """
    Checks if a shell script contains multiline commands.

    Args:
        script_text (str): The shell script code to check.

    Returns:
        bool: True if the script contains multiline commands, False otherwise.
    """    
    # Patterns that indicate a line continues
    continuation_patterns = [
        r"\\$",  # Line continuation character at the end of the line
        r"\|$",  # Pipe character at the end of the line indicating a pipeline continuation
        r"&&\s*$",  # Logical AND at the end of the line
        r"\|\|\s*$",  # Logical OR at the end of the line
        r"<\($",  # Start of process substitution
        r"\($",  # Start of subshell
        r"{\s*$",  # Start of a block
        r"\bif\b",  # Start of an if statement
        r"\bwhile\b",  # Start of a while loop
        r"\bfor\b",  # Start of a for loop
        r"do\s*$",  # 'do' keyword for loops
        r"then\s*$",  # 'then' keyword for if statements
    ]

    # Check each line for multiline patterns
    for line in script_text.splitlines():
        if any(re.search(pattern, line.rstrip()) for pattern in continuation_patterns):
            return True

    return False


if __name__ == '__main__':
    env = Shell()
    code = 'pip install --upgrade pip'
    for _ in env.run(code):
        print(_)
