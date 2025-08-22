# Windows-specific shell environment for OS-Copilot

import os
import platform
import queue
import re
import subprocess
import threading
import time
import traceback
from oscopilot.environments import SubprocessEnv


class WindowsShell(SubprocessEnv):
    """
    A class representing a Windows shell environment for executing commands.
    
    This class inherits from SubprocessEnv and provides Windows-specific
    command execution using either PowerShell or cmd.exe.
    """
    file_extension = "bat"
    name = "WindowsShell"
    aliases = ["windows", "cmd", "powershell", "ps"]
    
    def __init__(self, use_powershell=True):
        """
        Initializes the Windows shell environment.
        
        Args:
            use_powershell (bool): If True, uses PowerShell; otherwise uses cmd.exe
        """
        super().__init__()
        
        # Determine which shell to use
        if use_powershell and self._check_powershell_available():
            self.start_cmd = ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass"]
            self.shell_type = "powershell"
        else:
            self.start_cmd = ["cmd.exe"]
            self.shell_type = "cmd"
    
    def _check_powershell_available(self):
        """
        Checks if PowerShell is available on the system.
        
        Returns:
            bool: True if PowerShell is available, False otherwise
        """
        try:
            subprocess.run(["powershell", "-Command", "echo test"], 
                         capture_output=True, timeout=5)
            return True
        except (subprocess.SubprocessError, FileNotFoundError):
            return False
    
    def preprocess_code(self, code):
        """
        Preprocesses the Windows command/script before execution.
        
        Args:
            code (str): The Windows command or script to preprocess.
        
        Returns:
            str: The preprocessed command/script.
        """
        return preprocess_windows_command(code, self.shell_type)
    
    def line_postprocessor(self, line):
        """
        Postprocesses each line of output from Windows command execution.
        
        Args:
            line (str): A line from the output of command execution.
        
        Returns:
            str: The processed line.
        """
        # Remove Windows line endings and clean up output
        line = line.replace('\r\n', '\n').replace('\r', '\n')
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


def preprocess_windows_command(code, shell_type="cmd"):
    """
    Preprocesses Windows commands/scripts before execution.
    
    Args:
        code (str): The Windows command or script to preprocess.
        shell_type (str): The type of shell ("cmd" or "powershell")
    
    Returns:
        str: The preprocessed command/script.
    """
    
    # Add active line markers if not multiline
    if not has_multiline_commands(code):
        code = add_active_line_prints(code, shell_type)
    
    # Add end command marker
    if shell_type == "powershell":
        code += '\nWrite-Host "##end_of_execution##"'
    else:
        code += '\necho ##end_of_execution##'
    
    return code


def add_active_line_prints(code, shell_type="cmd"):
    """
    Adds echo/Write-Host statements indicating line numbers to a Windows script.
    
    Args:
        code (str): The Windows script to add active line indicators to.
        shell_type (str): The type of shell ("cmd" or "powershell")
    
    Returns:
        str: The modified script with active line indicators.
    """
    lines = code.split("\n")
    for index, line in enumerate(lines):
        # Skip empty lines
        if line.strip():
            if shell_type == "powershell":
                lines[index] = f'Write-Host "##active_line{index + 1}##"\n{line}'
            else:
                lines[index] = f'echo ##active_line{index + 1}##\n{line}'
    return "\n".join(lines)


def has_multiline_commands(script_text):
    """
    Checks if a Windows script contains multiline commands.
    
    Args:
        script_text (str): The Windows script to check.
    
    Returns:
        bool: True if the script contains multiline commands, False otherwise.
    """
    # Patterns that indicate multiline commands in Windows
    continuation_patterns = [
        r"\^$",  # Caret at end of line (cmd line continuation)
        r"`$",   # Backtick at end of line (PowerShell line continuation)
        r"\|$",  # Pipe at end of line
        r"&&\s*$",  # Logical AND at end of line
        r"\|\|\s*$",  # Logical OR at end of line
        r"\bif\b",  # Start of if statement
        r"\bfor\b",  # Start of for loop
        r"\bwhile\b",  # Start of while loop (PowerShell)
        r"\bforeach\b",  # Start of foreach loop (PowerShell)
        r"{\s*$",  # Opening brace (PowerShell script blocks)
    ]
    
    # Check each line for multiline patterns
    for line in script_text.splitlines():
        if any(re.search(pattern, line.rstrip(), re.IGNORECASE) 
               for pattern in continuation_patterns):
            return True
    
    return False


# Cross-platform command mapping
COMMAND_MAPPING = {
    'ls': {'cmd': 'dir', 'powershell': 'Get-ChildItem'},
    'pwd': {'cmd': 'cd', 'powershell': 'Get-Location'},
    'cat': {'cmd': 'type', 'powershell': 'Get-Content'},
    'rm': {'cmd': 'del', 'powershell': 'Remove-Item'},
    'cp': {'cmd': 'copy', 'powershell': 'Copy-Item'},
    'mv': {'cmd': 'move', 'powershell': 'Move-Item'},
    'mkdir': {'cmd': 'mkdir', 'powershell': 'New-Item -ItemType Directory'},
    'touch': {'cmd': 'type nul >', 'powershell': 'New-Item -ItemType File'},
    'grep': {'cmd': 'findstr', 'powershell': 'Select-String'},
    'which': {'cmd': 'where', 'powershell': 'Get-Command'},
    'clear': {'cmd': 'cls', 'powershell': 'Clear-Host'},
}


def translate_unix_to_windows(command, shell_type="cmd"):
    """
    Translates common Unix commands to Windows equivalents.
    
    Args:
        command (str): The Unix command to translate
        shell_type (str): The target Windows shell type
    
    Returns:
        str: The Windows equivalent command
    """
    parts = command.split()
    if parts and parts[0] in COMMAND_MAPPING:
        windows_cmd = COMMAND_MAPPING[parts[0]][shell_type]
        if len(parts) > 1:
            # Append arguments
            return f"{windows_cmd} {' '.join(parts[1:])}"
        return windows_cmd
    return command


if __name__ == '__main__':
    # Test the Windows shell environment
    env = WindowsShell()
    test_commands = [
        'echo Hello from Windows',
        'dir',
        'cd'
    ]
    
    for cmd in test_commands:
        print(f"\nExecuting: {cmd}")
        for output in env.run(cmd):
            if output.get('content'):
                print(output['content'], end='')