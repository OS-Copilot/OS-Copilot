import os
from oscopilot.environments import SubprocessEnv


class AppleScript(SubprocessEnv):
    """
    A class representing an AppleScript environment for executing AppleScript code.

    This class inherits from SubprocessEnv, which provides a general environment for executing code in subprocesses.
    """    
    file_extension = "applescript"
    name = "AppleScript"

    def __init__(self):
        """
        Initializes the AppleScript environment.

        Sets up the start command for executing AppleScript code.
        """        
        super().__init__()
        self.start_cmd = [os.environ.get("SHELL", "/bin/zsh")]

    def preprocess_code(self, code):
        """
        Preprocesses the AppleScript code before execution.

        Inserts an end_of_execution marker and adds active line indicators to the code.

        Args:
            code (str): The AppleScript code to preprocess.

        Returns:
            str: The preprocessed AppleScript code.
        """
        # Add active line indicators to the code
        code = self.add_active_line_indicators(code)

        # Escape double quotes
        code = code.replace('"', r"\"")

        # Wrap in double quotes
        code = '"' + code + '"'

        # Prepend start command for AppleScript
        code = "osascript -e " + code

        # Append end of execution indicator
        code += '; echo "##end_of_execution##"'

        return code

    def add_active_line_indicators(self, code):
        """
        Adds log commands to indicate the active line of execution in the AppleScript.

        Args:
            code (str): The AppleScript code to add active line indicators to.

        Returns:
            str: The modified AppleScript code with active line indicators.
        """
        modified_lines = []
        lines = code.split("\n")

        for idx, line in enumerate(lines):
            # Add log command to indicate the line number
            if line.strip():  # Only add if line is not empty
                modified_lines.append(f'log "##active_line{idx + 1}##"')
            modified_lines.append(line)

        return "\n".join(modified_lines)

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
