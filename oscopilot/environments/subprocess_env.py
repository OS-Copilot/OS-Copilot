import os
import queue
import re
import subprocess
import threading
import time
import traceback
from oscopilot.environments.base_env import BaseEnv

class SubprocessEnv(BaseEnv):
    """
    A class representing an environment for executing code using subprocesses.

    This class manages the execution of code in subprocesses, providing methods for preprocessing code,
    starting and terminating processes, handling output streams, and executing code steps.

    It inherits from BaseEnv, which provides basic environment functionality.
    """    

    def __init__(self):
        """
        Initializes the subprocess environment.

        Attributes:
            start_cmd (list): The command used to start the subprocess.
            process (subprocess.Popen or None): The subprocess object.
            verbose (bool): Whether to print verbose output.
            output_queue (queue.Queue): A queue for storing output messages.
            done (threading.Event): An event to signal completion of execution.
        """        
        self.start_cmd = []
        self.process = None
        self.verbose = False
        self.output_queue = queue.Queue()
        self.done = threading.Event()

    def detect_active_line(self, line):
        """
        Detects an active line indicator in the output line.

        Args:
            line (str): The output line from the subprocess.

        Returns:
            int or None: The active line number if detected, else None.
        """        
        return None

    def detect_end_of_execution(self, line):
        """
        Detects an end of execution marker in the output line.

        Args:
            line (str): The output line from the subprocess.

        Returns:
            bool: True if end of execution marker is detected, else False.
        """        
        return None

    def line_postprocessor(self, line):
        """
        Post-processes an output line from the subprocess.

        Args:
            line (str): The output line from the subprocess.

        Returns:
            str or None: The processed line or None if line should be discarded.
        """        
        return line

    def preprocess_code(self, code):
        """
        Preprocesses code before execution.

        This method inserts an end_of_execution marker and optionally adds active line markers.

        Args:
            code (str): The code to preprocess.

        Returns:
            str: The preprocessed code.
        """
        return code

    def terminate(self):
        """
        Terminates the subprocess if it is running.
        """        
        if self.process:
            self.process.terminate()
            self.process.stdin.close()
            self.process.stdout.close()

    def start_process(self):
        """
        Starts the subprocess to execute code.
        """        
        if self.process:
            self.terminate()

        my_env = os.environ.copy()
        my_env["PYTHONIOENCODING"] = "utf-8"
        self.process = subprocess.Popen(
            self.start_cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=0,
            universal_newlines=True,
            env=my_env,
            encoding="utf-8",
            errors="replace",
        )
        threading.Thread(
            target=self.handle_stream_output,
            args=(self.process.stdout, False),
            daemon=True,
        ).start()
        threading.Thread(
            target=self.handle_stream_output,
            args=(self.process.stderr, True),
            daemon=True,
        ).start()

    def step(self, code):
        """
        Executes a step of code.

        Args:
            code (str): The code to execute.

        Yields:
            dict: Output messages generated during execution.
        """        
        retry_count = 0
        max_retries = 3

        # Setup
        try:
            code = self.preprocess_code(code)
            if not self.process:
                self.start_process()
        except:
            yield {
                "type": "console",
                "format": "output",
                "content": traceback.format_exc(),
            }
            return

        while retry_count <= max_retries:
            if self.verbose:
                print(f"(after processing) Running processed code:\n{code}\n---")

            self.done.clear()

            try:
                self.process.stdin.write(code + "\n")
                self.process.stdin.flush()
                break
            except:
                if retry_count != 0:
                    # For UX, I like to hide this if it happens once. Obviously feels better to not see errors
                    # Most of the time it doesn't matter, but we should figure out why it happens frequently with:
                    # applescript
                    yield {
                        "type": "console",
                        "format": "output",
                        "content": f"{traceback.format_exc()}\nRetrying... ({retry_count}/{max_retries})\nRestarting process.",
                    }

                self.start_process()

                retry_count += 1
                if retry_count > max_retries:
                    yield {
                        "type": "console",
                        "format": "output",
                        "content": "Maximum retries reached. Could not execute code.",
                    }
                    return

        while True:
            if not self.output_queue.empty():
                yield self.output_queue.get()
            else:
                time.sleep(0.1)
            try:
                output = self.output_queue.get(timeout=0.3)  # Waits for 0.3 seconds
                yield output
            except queue.Empty:
                if self.done.is_set():
                    # Try to yank 3 more times from it... maybe there's something in there...
                    # (I don't know if this actually helps. Maybe we just need to yank 1 more time)
                    for _ in range(3):
                        if not self.output_queue.empty():
                            yield self.output_queue.get()
                        time.sleep(0.2)
                    break

    def handle_stream_output(self, stream, is_error_stream):
        """
        Handles the streaming output from the subprocess.

        Args:
            stream: The output stream to handle.
            is_error_stream (bool): Indicates if the stream is the error stream.
        """        
        try:
            for line in iter(stream.readline, ""):
                if self.verbose:
                    print(f"Received output line:\n{line}\n---")

                line = self.line_postprocessor(line)

                if line is None:
                    continue  # `line = None` is the postprocessor's signal to discard completely

                if self.detect_active_line(line):
                    active_line = self.detect_active_line(line)
                    self.output_queue.put(
                        {
                            "type": "console",
                            "format": "active_line",
                            "content": active_line,
                        }
                    )
                    # Sometimes there's a little extra on the same line, so be sure to send that out
                    line = re.sub(r"##active_line\d+##", "", line)
                    if line:
                        self.output_queue.put(
                            {"type": "console", "format": "output", "content": line}
                        )
                elif self.detect_end_of_execution(line):
                    # Sometimes there's a little extra on the same line, so be sure to send that out
                    line = line.replace("##end_of_execution##", "").strip()
                    if line:
                        self.output_queue.put(
                            {"type": "console", "format": "output", "content": line}
                        )
                    self.done.set()
                elif is_error_stream and "KeyboardInterrupt" in line:
                    self.output_queue.put(
                        {
                            "type": "console",
                            "format": "output",
                            "content": "KeyboardInterrupt",
                        }
                    )
                    time.sleep(0.1)
                    self.done.set()
                else:
                    self.output_queue.put(
                        {"type": "console", "format": "output", "content": line}
                    )
        except ValueError as e:
            if "operation on closed file" in str(e):
                if self.verbose:
                    print("Stream closed while reading.")
            else:
                raise e


