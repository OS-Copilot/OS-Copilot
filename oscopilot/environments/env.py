# This code is based on Open Interpreter. Original source: https://github.com/OpenInterpreter/open-interpreter

from oscopilot.environments import BaseEnv
from oscopilot.environments import AppleScript
from oscopilot.environments import PythonJupyterEnv
from oscopilot.environments import Shell
from oscopilot.utils.schema import EnvState
import subprocess

# Should this be renamed to OS or System?


class Env(BaseEnv):
    """
    A class representing an environment for executing code in various languages.

    This class manages the execution of code in different languages and provides methods for interacting with
    those languages.

    It inherits from BaseEnv, which provides basic environment functionality.
    """    
    def __init__(self):
        """
        Initializes the environment.

        Sets up the supported languages and initializes the active languages dictionary.
        """        
        super().__init__()
        self.languages = [
            PythonJupyterEnv,
            Shell,
            AppleScript,
        ]
        self._active_languages = {}

    def get_language(self, language):
        """
        Gets the language class based on the provided language name or alias.

        Args:
            language (str): The name or alias of the language.

        Returns:
            class: The language class corresponding to the provided name or alias, or None if not found.
        """        
        # 输入planner的节点类型即可
        for lang in self.languages:
            if language.lower() == lang.name.lower() or (
                hasattr(lang, "aliases") and language.lower() in (alias.lower() for alias in lang.aliases)
            ):
                return lang
        return None

    def step(self, language, code, stream=False, display=False):
        """
        Executes a step of code in the specified language.

        Args:
            language (str): The name or alias of the language to execute the code in.
            code (str): The code to execute.
            stream (bool): Whether to stream the output as it becomes available.
            display (bool): Whether to display the output.

        Returns:
            EnvState: The state after executing the code.
        """        
        # 不用流式的话很简单，就是调一下lang的step就行了
        state = EnvState(command=code)
        lang = self.get_language(language)()  # 输入planner的节点类型即可
        for output_line_dic in lang.step(code):
            if output_line_dic['format'] == 'active_line' or output_line_dic['content'] in ['', '\n']:
                continue
            content = output_line_dic['content']
            if 'Traceback' in content:
                state.error = (state.error or '') + content
            else:
                state.result += content
        if lang.name == 'Python':
            lang.terminate()
        # for output_line_dic in lang.step(code):
        #     if output_line_dic['format'] == 'active_line':
        #         continue
        #     content = output_line_dic['content']
        #     if content != '' and content != '\n':
        #         if 'Traceback' in content:
        #             state.error = (state.error or '') + content
        #         else:
        #             state.result += content
        state.pwd = self.working_dir
        state.ls = subprocess.run(['ls'], cwd=self.working_dir, capture_output=True, text=True).stdout
        return state
        
        # if (
        #     language == "python"
        #     and self.computer.import_computer_api
        #     and "computer" in code
        # ):
        #     if not self.computer._has_imported_computer_api:
        #         self.computer._has_imported_computer_api = True
        #         # Give it access to the computer via Python
        #         self.computer.run(
        #             language="python",
        #             code="import time\nfrom interpreter import interpreter\ncomputer = interpreter.computer",  # We ask it to use time, so
        #             display=self.computer.verbose,
        #         )

        if stream == False:
            # If stream == False, *pull* from _streaming_run.
            output_messages = []
            for chunk in self._streaming_run(language, code, display=display):
                if chunk.get("format") != "active_line":
                    # Should we append this to the last message, or make a new one?
                    if (
                        output_messages != []
                        and output_messages[-1].get("type") == chunk["type"]
                        and output_messages[-1].get("format") == chunk["format"]
                    ):
                        output_messages[-1]["content"] += chunk["content"]
                    else:
                        output_messages.append(chunk)
            return output_messages

        elif stream == True:
            # If stream == True, replace this with _streaming_run.
            return self._streaming_run(language, code, display=display)

    def _streaming_run(self, language, code, display=False):
        """
        Executes code in the specified language and streams the output.

        Args:
            language (str): The name or alias of the language to execute the code in.
            code (str): The code to execute.
            display (bool): Whether to display the output.

        Yields:
            dict: Output chunks generated during execution.
        """        
        if language not in self._active_languages:
            # Get the language. Pass in self.computer *if it takes a single argument*
            # but pass in nothing if not. This makes custom languages easier to add / understand.
            lang_class = self.get_language(language)
            if lang_class.__init__.__code__.co_argcount > 1:
                self._active_languages[language] = lang_class(self.computer)
            else:
                self._active_languages[language] = lang_class()
        try:
            for chunk in self._active_languages[language].run(code):
                # self.format_to_recipient can format some messages as having a certain recipient.
                # Here we add that to the LMC messages:
                if chunk["type"] == "console" and chunk.get("format") == "output":
                    recipient, content = parse_for_recipient(chunk["content"])
                    if recipient:
                        chunk["recipient"] = recipient
                        chunk["content"] = content

                    # Sometimes, we want to hide the traceback to preserve tokens.
                    # (is this a good idea?)
                    if "@@@HIDE_TRACEBACK@@@" in content:
                        chunk["content"] = (
                            "Stopping execution.\n\n"
                            + content.split("@@@HIDE_TRACEBACK@@@")[-1].strip()
                        )

                yield chunk

                # Print it also if display = True
                if (
                    display
                    and chunk.get("format") != "active_line"
                    and chunk.get("content")
                ):
                    print(chunk["content"])

        except GeneratorExit:
            self.stop()

    def stop(self):
        """
        Stops the execution of all active languages.
        """        
        for language in self._active_languages.values():
            language.stop()

    def terminate(self):
        """
        Terminates all active language environments.
        """        
        for language_name in list(self._active_languages.keys()):
            language = self._active_languages[language_name]
            if (
                language
            ):  # Not sure why this is None sometimes. We should look into this
                language.terminate()
            del self._active_languages[language_name]
