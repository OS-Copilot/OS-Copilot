from jarvis.action.base_action import BaseAction


class turn_on_dark_mode(BaseAction):
    def __init__(self) -> None:
        super().__init__()
        self._description = "Using turn_on_dark_mode() will change your system into the dark mode."
        self.action_type = 'BASH'

    def __call__(self, *args, **kwargs):
        return 'shortcuts run "Dark Mode"'

    # @property
    # def _command(self):
    #     return 'shortcuts run "Dark Mode"'
        # return self._python(
        #     self._import("atom", "operations"),
        #     "adjust_theme('Adwaita-dark')"
        # )

    # def _success(self):
    #     return "Successfully turned the system into the Dark Mode"

    # def __call__(self, *args, **kwargs):
    #
    #     command = 'shortcuts run "Dark Mode"'
    #     try:
    #         # result = subprocess.run([command, "Dark Mode"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    #         result = subprocess.run([command], capture_output=True, check=True,
    #                                 text=True, shell=True, timeout=self.timeout, stdin=subprocess.DEVNULL)
    #         if result.returncode == 0:
    #             return result
    #     except subprocess.CalledProcessError as e:
    #         return e
        # except subprocess.TimeoutExpired:
        #     raise TimeoutError(f"Command '{command}' timed out after {self.timeout} seconds.")
