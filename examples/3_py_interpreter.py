from jarvis.action_lib.python_interpreter import PythonInterpreter, DEFAULT_DESCRIPTION


# a = PythonInterpreter()
# a(DEFAULT_DESCRIPTION)

import subprocess
import os

# 执行 cd 命令
current_dir = os.getcwd()
print("当前工作目录：", current_dir)

command = 'gogogo && cd .. && pwd'
result = subprocess.run(command, shell=True, capture_output=True, text=True)
stout = result.stdout.strip().split('\n')
out = "\n".join(stout[:-1])
pwd = stout[-1]

print("out", out)
print("pwd", pwd)
print(result.stderr)

# 打印当前目录
print("当前目录：", current_dir)
#
# self.env_state = EnvState()
#         self.env_state.command.append(_command)
#         command = _command + self.log_execute
#         subprocess.run(["tmux", "send-keys", "-t", self.server_name, command, "Enter"])
#         time.sleep(self.timeout)
#         self.observe()
#         return self.env_state
#
#
# command = "pwd" + self.log_state
#         subprocess.run(["tmux", "send-keys", "-t", self.server_name, command, "Enter"])
#         time.sleep(1)
#         self.env_state.pwd = self.read_log(self.state_log_path)
#         self.working_dir = self.env_state.pwd[0].strip()
#         # print("working dir:", self.working_dir)
#         result = subprocess.run(['ls'], cwd=self.working_dir, capture_output=True, text=True)
#         self.env_state.ls = [result.stdout]
#         # 输出执行结果
#         # print(result.stdout)
#         # for _command in ["pwd", "ls"]:
#         #     command = _command + self.log_state
#         #     subprocess.run(["tmux", "send-keys", "-t", self.server_name, command, "Enter"])
#         #     # todo 处理异步的问题，可能提交过去还没执行完。
#         #     time.sleep(self.timeout)
#         #     if _command == "pwd":
#         #         self.env_state.pwd = self.read_log(self.state_log_path)
#         #     else:
#         #         self.env_state.ls = self.read_log(self.state_log_path)
#         self.env_state.result = self.read_log(self.execute_log_path)