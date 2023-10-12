from jarvis.action.turn_on_dark_mode import turn_on_dark_mode
from jarvis.action.organize_app_layout import organize_app_layout
import subprocess
# import os
#
# functions = {"turn_on_dark_mode()": turn_on_dark_mode(), "turn_on_dark_mode()":organize_app_layout()}
# functions["turn_on_dark_mode()"].run()
organize_app_layout().run()
# command = 'shortcuts run "Dark Mode"'
# # command = 'du -d 1 -h'
# # subprocess.run([command], text=True, shell=True)
# # os.system(command)
# os.popen(command)
# try:
#     # 执行命令
#     cmd_output = os.popen(command).read()
# except Exception as e:
#     # 捕获异常并处理
#     print("An error occurred:\n", str(e))
# else:
#     # 没有发生异常时执行的代码
#     print("Command output:\n", cmd_output)

# import subprocess
#
# try:
#     # 执行命令
#     result = subprocess.run(['shortcuts', 'run', 'Dark Mode'], capture_output=True, text=True, stdin=subprocess.DEVNULL)
#     result.check_returncode()  # 检查命令的返回码
# except subprocess.CalledProcessError as e:
#     # 命令执行失败时的异常处理
#     print("Command failed with return code:", e.returncode)
#     print("Command output:", e.stdout)
# except Exception as e:
#     # 其他异常处理
#     print("An error occurred:", str(e))
# else:
#     # 没有发生异常时执行的代码
#     print("Command output:", result.stdout)