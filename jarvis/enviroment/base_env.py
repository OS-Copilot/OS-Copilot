import subprocess
import time
import os
from typing import Optional, Union, List
from jarvis.agent.base_agent import BaseAgent
from jarvis.core.schema import ActionReturn, ActionStatusCode, EnvState
import asyncio


class BaseEnviroment:
    """Base class for all actions.

    Args:
        description (str, optional): The description of the action. Defaults to
            None.
        name (str, optional): The name of the action. If None, the name will
            be class name. Defaults to None.
    """

    def __init__(self,
                 name: Optional[str] = None,
                 timeout: Optional[int] = 2,
                 execute_log_path: Optional[str] = "execute.log",
                 state_log_path: Optional[str] = "state.log",
                 logging_command: Optional[str] = " 2>&1 | tee ") -> None:
        if name is None:
            name = self.__class__.__name__
        self._name = name
        self.timeout = timeout
        self.execute_log_path = execute_log_path
        self.state_log_path = state_log_path
        self.working_dir = os.path.abspath(os.path.join(__file__, "..", "..", "..", "working_dir"))
        self.log_execute = logging_command + os.path.join(self.working_dir, self.execute_log_path)
        self.log_state = logging_command + os.path.join(self.working_dir, self.state_log_path)
        self.server_name = "test"
        self.env_state = None
        # print(self.working_dir)
        # self.init_env()

    def init_env(self):
        # cur_dir = os.getcwd()
        # os.chdir(self.working_dir)
        # command = "tmux new-session -d -s " + self.server_name
        # os.system(command)
        # os.chdir(cur_dir)
        # todo catch new duplicate session error
        subprocess.run(["tmux", "new-session", "-d", "-s", self.server_name], cwd=self.working_dir)
        output = subprocess.check_output(["tmux", "ls"]).decode("utf-8")
        # output = subprocess.run(["tmux ls"], capture_output=True, shell=True, text=True)
        # print(output)
        # todo add raise error
        if self.server_name not in output:
            return False, "Error: init server failed"
        else:
            return True, "Init tmux server, done."

    def execute_command(self, command):
        subprocess.run(["tmux", "send-keys", "-t", self.server_name, command, "Enter"])

    def step(self, _command) -> EnvState:
        self.env_state = EnvState()
        self.env_state.command.append(_command)
        command = _command + self.log_execute
        subprocess.run(["tmux", "send-keys", "-t", self.server_name, command, "Enter"])
        time.sleep(self.timeout)
        self.observe()
        return self.env_state

    def read_log(self, log_path):
        os.chdir(self.working_dir)
        with open(log_path) as f:
            return f.readlines()

    def observe(self) -> None:
        command = "pwd" + self.log_state
        subprocess.run(["tmux", "send-keys", "-t", self.server_name, command, "Enter"])
        time.sleep(1)
        self.env_state.pwd = self.read_log(self.state_log_path)
        self.working_dir = self.env_state.pwd[0].strip()
        # print("working dir:", self.working_dir)
        result = subprocess.run(['ls'], cwd=self.working_dir, capture_output=True, text=True)
        self.env_state.ls = [result.stdout]
        # 输出执行结果
        # print(result.stdout)
        # for _command in ["pwd", "ls"]:
        #     command = _command + self.log_state
        #     subprocess.run(["tmux", "send-keys", "-t", self.server_name, command, "Enter"])
        #     # todo 处理异步的问题，可能提交过去还没执行完。
        #     time.sleep(self.timeout)
        #     if _command == "pwd":
        #         self.env_state.pwd = self.read_log(self.state_log_path)
        #     else:
        #         self.env_state.ls = self.read_log(self.state_log_path)
        self.env_state.result = self.read_log(self.execute_log_path)
        # print(self.env_state)
    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    def __repr__(self):
        return f'{self.name}:{self.description}'

    def __str__(self):
        return self.__repr__()


if __name__ == '__main__':
    env = BaseEnviroment()
    env.env_state = EnvState()
    result = env.observe()
