skillCreator = LinuxSkillCreator(config_path="../../examples/config.json")
task = "Please download the audio I have given link from the Internet to the desktop of the system and play it in the system."
python_code = skillCreator.format_message(task)
if '```python' in python_code:
    python_code = python_code.split('```python')[1].split('```')[0]
elif '```' in python_code:
    python_code = python_code.split('```')[1].split('```')[0]
file_name = "my_python_script.py"

# 打开文件并写入代码字符串
with open(file_name, "w") as file:
    file.write(python_code)

print(f"The Python code has been saved to {file_name}")