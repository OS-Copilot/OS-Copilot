# This code is based on Open Interpreter. Original source: https://github.com/OpenInterpreter/open-interpreter

from oscopilot.utils import setup_config, setup_pre_run
from oscopilot.modules.base_module import BaseModule
import re
from rich.console import Console
from rich.markdown import Markdown
import dotenv
import os

# newly added imports
from PIL import ImageGrab
from datetime import datetime
import base64
import requests
import pyautogui

dotenv.load_dotenv(override=True)
MODEL_NAME = os.getenv('MODEL_NAME')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_ORGANIZATION = os.getenv('OPENAI_ORGANIZATION')
BASE_URL = os.getenv('OPENAI_BASE_URL')
OCR_ACCESS_KEY = '' # your access token for OCR API

console = Console()

def rich_print(markdown_text):
    md = Markdown(markdown_text)
    console.print(md)


def send_chat_prompts(message, llm):
    return llm.chat(message)

# new function to transcribe user's vocal input into text transcript
def send_initial_request(speech, llm):
    return llm.listen(speech)
    
def extract_code(input_string):
    pattern = r"```(\w+)?\s*(.*?)```"  
    matches = re.findall(pattern, input_string, re.DOTALL)

    if matches:
        language, code = matches[0]

        if not language:
            if re.search("python", code.lower()) or re.search(r"import\s+\w+", code):
                language = "Python"
            elif re.search("bash", code.lower()) or re.search(r"echo", code):
                language = "Bash"

        return code.strip(), language
    else:
        return None, None
    
def ocr(image_path):
    '''
    Generates a dictionary of words and their respective coordinates in the image and an encoded image for API requests.

    Args:
        image_path (str): path to the image file
        
    Returns:
        dict: dictionary of words and their respective coordinates in the image
        str: encoded image for API requests
    '''
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general" 
    f = open(image_path, 'rb')
    img = base64.b64encode(f.read())
    params = {"image": img, 'paragraph': 'false', 'probability': 'false'}
    access_token = OCR_ACCESS_KEY 
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        if response.json()['words_result']:
            dict = {}
            for item in response.json()['words_result']:
                dict[item['words']] = (item['location']['left'] + item['location']['width'] // 2, item['location']['top'] + item['location']['height'] // 2)
            return (dict, img.decode('utf-8'))
        else:
            raise Exception("No words found in the image")
    else:
        raise Exception("OCR failed")
    

class LightFriday(BaseModule):
    def __init__(self, args):
        super().__init__()
        self.args = args
    
    def execute_tool(self, code, lang):
        state = self.environment.step(lang, code)  # node_type
        return_info = ''
        if state.result != None and state.result.strip() != '':
            return_info = '**Execution Result** :' + state.result.strip()
        if state.error != None and state.error.strip() != '':
            return_info = '\n**Execution Error** :' + state.error.strip()
        return return_info.strip()
    

    def run(self, task):
        light_planner_sys_prompt = '''
        You are Light Friday, a world-class programmer that can complete any goal by executing code. You will act as an agent and perform desktop computer tasks.
Also you are equipped with good knowledge of computer and good internet connection and assume your code will run on a computer for controlling the mouse and keyboard.
First, write a plan. **Always recap the plan between each code block** (you have extreme short-term memory loss, so you need to recap the plan between each message block to retain it).
-- General Rules for Execution:
When you execute code, it will be executed **on the user's machine**. The user has given you **full and complete permission** to execute any code necessary to complete the task. Execute the code.
To interact with the user's machine, primarily use the **PyAutoGUI** package to control the mouse and keyboard. If **PyAutoGUI** is not installed in the environment, ensure you install it using pip (`pip install pyautogui`) before proceeding.
At each step, you will receive a screenshot of the entire current computer screen with the coordinates of the file or folder labeled packaged in a dictionary for reference, all together denoted as an "observation". **Analyzing the content of the screenshot is your only way to see what is happening and that will serve as a guide for your mouse and keyboard actions**. You should always assume that the screenshot will be provided and you should never ask 'Please provide the screenshot' in the planning/reporting.
If the screenshot indicates that your previous operation didn't work as expected, try to adjust to address the previous operation first before continue to the next step according to the plan.
**DO NOT USE** the `pyautogui.locateCenterOnScreen` function to locate the element you want to operate with given no image of the element you want to operate with. Also, **DO NOT USE** `pyautogui.screenshot()` to make screenshot as all the screenshot images will be provided to you.
When locating according to the coordinates, you should always move your mouse to the central coordinate of the icon/entry/representation of the file/folder/element** you want to operate with according to the respective tasks, if you are moving the mouse. The central coordinates are provided to you in the dictionary.
**NEVER ASSUME** one action is successfully executed
You can only deduce from the last observation if the last action was executed successfully.
When user's request is finished one time, you should **TERMINATE IMMEDIATELY** after necessary checking. **DO NOT** keep the program running indefinitely.
If you want to send data between programming languages, save the data to a txt or json.

-- Some **RESTRICTIONS** regarding interacting with the user's machine:
1. When you want to open an file **NOT FROM SEARCHING**, you should always right click. Then you should locate and navigate to 'Open' to open the file. 
1.1 If you are openning a file **FROM SEARCHING**, you should **ALWAYS CLICK or PRESS ENTER**.
2. In tasks involving opening a file, always make sure the file is opened by checking the observations before proceeding to any further operation.
3. If the window you are interfacing with is not maximized, **MAXIMIZE the WINDOW by CLICKING FIRST**.
4. Take multiple steps to ensure your opeartion is successful, **check after every step**. Successful is defined as 4.1 and 4.2.
4.1 If you are opening a file/folder, make sure you can see the file/folder in the observation before proceeding.
4.2 If you are performing any write-in operation, make sure you can see the content being written in the observation, before proceeding.
5. In addition, you may utilize right click to perform some other actions according to need.
6. **DO NOT USE** `pyautogui.hotkey()` **BUT USE** `pyautogui.keyDown()` and `pyautogui.keyUp()` for using **ANY KEY COMBINATION** as shortcut.
7. Always save the file before terminating actions if any write-in operation is performed.
8. Never attempt to rename file/folder/element unless prompted by the user, in which case you need to closely follow user's provided name and always check the extension name according to observation before confirming with enter(make sure no duplicating or wrong extension name occurs).
9. Always close the window by clicking the close button.
10. If any new file generated, the icon of which overlaps with other icons, you should always drag the new file to a different location to avoid overlapping with any other icons.

-- Some **RESTRICTIONS** on locating the correct file or folder:
1. When a user refers to a filename, they're likely referring to an existing file or folder in the directory you're currently executing code in. 
2. The file or folder could be in other directories on the user's machine not visible to you in the current observation, in which case you need to **search for it on the user's machine and locate it**. This should be done via searching the file or folder name in the file explorer or using the command line.
3. If operating on OSX system, you are welcome to use the 'Spotlight' feature by hitting command + space to do searching. **DO NOT USE** mouse clicks to open an **INSTALLED APPLICATION**, instead **ALWAYS USE** searching. You **should use terminal commands** like `find` or `locate` to search for the file or folder if the aforementioned searching doesn't work.
4. You need to determine the target file or folder given the filename in the user input which may not be complete or correctly spelled. You need to **decide the file or the folder most likely to match the user-given filename**, in the process of which you might take a few different attempts to locate the file.
Write messages to the user in Markdown.

-- Some **RESTRICTIONS** on searching online:
1. You should always open the search engine in the user's default browser. Only use other when specified
2. You should always open a new tab for each search.

In general, try to **make plans** with as few steps as possible. As for actually executing code to carry out that plan, for *stateful* languages (like python, javascript, shell, but NOT for html which starts from 0 every time) **it's critical not to try to do everything in one code block.** You should try something, print information about it, then continue from there in tiny, informed steps. You will never get it on the first try, and attempting it in one go will often lead to errors you cant see.
You are capable of **any** task.
You can access the internet. Run **any code** to achieve the goal, and if at first you don't succeed, try again and again.
Include a comment in your code blocks to specify the programming language used, like this:
```python
# This code is written in Python
print("hello, world")
```
Currently, supported languages include Python and Bash."
'''  
#  Try to use `print` or `echo` to output information needed for the subsequent tasks, or the next step might not get the required information.
        light_planner_user_prompt = '''
        User's information are as follows:
        System Version: {system_version}
        Task: {task}
        Current Working Directiory: {working_dir}'''.format(system_version=self.system_version, task=task, working_dir=self.environment.working_dir)
        message = [
            {"role": "system", "content": light_planner_sys_prompt},
            {"role": "user", "content": light_planner_user_prompt},
        ]
        os.makedirs(os.path.join(self.environment.working_dir, 'observations'), exist_ok=True)
        ob_dir = os.path.join(self.environment.working_dir, 'observations')
        while True:
            screenshot = ImageGrab.grab()
            ob_name = "observation_{t}.png".format(t=datetime.now().strftime("%Y%m%d+%H%M%S"))
            img_path = os.path.join(ob_dir, ob_name)
            re_shot = screenshot.resize(pyautogui.size())
            re_shot.save(img_path, format='PNG')
            label_dict, encoded_image = ocr(img_path)
            message.append({
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Given the screenshot, Consider if the last action has been successfully executed and what's the next step that you will do to help with the task?"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{encoded_image}",
                                "detail": "high"
                            }
                        },
                        {
                            "type": "text", 
                            "text": "You may refer the dictionary together with the screenshot for better understanding the coordinates of the relevant files or folders or other information involved in the task:\n{}".format(label_dict)
                        }
                    ]
                })
            response = send_chat_prompts(message, self.llm)
            rich_print(response)
            message.append({"role": "system", "content": response})

            code, lang = extract_code(response)
            if code:
                result = self.execute_tool(code, lang)
                rich_print(result)
            else:
                result = ''

            if result != '':
                light_exec_user_prompt = 'The result after executing the code: {result}'.format(result=result)
                message.append({"role": "user", "content": light_exec_user_prompt})
            else:
                message.append({"role": "user", "content": "Please continue. If all tasks have been completed, reply with 'Execution Complete'. If you believe subsequent tasks cannot continue, reply with 'Execution Interrupted', including the reasons why the tasks cannot proceed, and provide the user with some possible solutions."})
            
            if 'Execution Complete' in response or 'Execution Interrupted' in response:
                break


args = setup_config()
if not args.query:
    args.query = "Plot AAPL and META's normalized stock prices"
task = setup_pre_run(args)

light_friday = LightFriday(args)
light_friday.run(task)  # list
