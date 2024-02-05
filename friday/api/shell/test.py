import requests
import json

base_url = 'http://localhost:8079'

def run_shell_command(command):
    response = requests.post(f'{base_url}/tools/shell', data=json.dumps({"command": command}), headers={'Content-Type': 'application/json'})
    if response.status_code == 200:
        print("Command executed successfully")
        print("STDOUT: ", response.json()['stdout'])
        print("STDERR: ", response.json()['stderr'])
    else:
        print("Error occurred while executing the command")

# Create the file in /root directory
run_shell_command("echo 'This is a test file.' > /root/test.txt")

# Copy the file to the current directory
run_shell_command("cp /root/test.txt ./test2.txt")
