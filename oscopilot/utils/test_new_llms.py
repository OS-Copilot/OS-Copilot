# This code is based on Open Interpreter. Original source: https://github.com/OpenInterpreter/open-interpreter


import base64
import io
import os
import json
import time

from PIL import Image

from rich import print as rich_print
from rich.markdown import Markdown
from rich.rule import Rule

from dotenv import load_dotenv

import litellm
import tokentrim as tt
litellm.suppress_debug_info = True


load_dotenv(dotenv_path='.env', override=True)
MODEL_NAME = os.getenv('MODEL_NAME')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_ORGANIZATION = os.getenv('OPENAI_ORGANIZATION')
BASE_URL = os.getenv('OPENAI_BASE_URL')


function_schema = {
    "name": "execute",
    "description": "Executes code on the user's machine **in the users local environment** and returns the output",
    "parameters": {
        "type": "object",
        "properties": {
            "language": {
                "type": "string",
                "description": "The programming language (required parameter to the `execute` function)",
                "enum": [
                    # This will be filled dynamically with the languages OI has access to.
                ],
            },
            "code": {"type": "string", "description": "The code to execute (required)"},
        },
        "required": ["language", "code"],
    },
}


def parse_partial_json(s):
    # Attempt to parse the string as-is.
    try:
        return json.loads(s)
    except:
        pass

    # Initialize variables.
    new_s = ""
    stack = []
    is_inside_string = False
    escaped = False

    # Process each character in the string one at a time.
    for char in s:
        if is_inside_string:
            if char == '"' and not escaped:
                is_inside_string = False
            elif char == "\n" and not escaped:
                char = "\\n"  # Replace the newline character with the escape sequence.
            elif char == "\\":
                escaped = not escaped
            else:
                escaped = False
        else:
            if char == '"':
                is_inside_string = True
                escaped = False
            elif char == "{":
                stack.append("}")
            elif char == "[":
                stack.append("]")
            elif char == "}" or char == "]":
                if stack and stack[-1] == char:
                    stack.pop()
                else:
                    # Mismatched closing character; the input is malformed.
                    return None

        # Append the processed character to the new string.
        new_s += char

    # If we're still inside a string at the end of processing, we need to close the string.
    if is_inside_string:
        new_s += '"'

    # Close any remaining open structures in the reverse order that they were opened.
    for closing_char in reversed(stack):
        new_s += closing_char

    # Attempt to parse the modified string as JSON.
    try:
        return json.loads(new_s)
    except:
        # If we still can't parse the string as JSON, return None to indicate failure.
        return None


def merge_deltas(original, delta):
    """
    Pushes the delta into the original and returns that.

    Great for reconstructing OpenAI streaming responses -> complete message objects.
    """

    for key, value in dict(delta).items():
        if value != None:
            if isinstance(value, str):
                if key in original:
                    original[key] = (original[key] or "") + (value or "")
                else:
                    original[key] = value
            else:
                value = dict(value)
                if key not in original:
                    original[key] = value
                else:
                    merge_deltas(original[key], value)

    return original


def run_function_calling_llm(llm, request_params):
    ## Setup

    # # Add languages OI has access to
    # function_schema["parameters"]["properties"]["language"]["enum"] = [
    #     i.name.lower() for i in llm.interpreter.computer.terminal.languages
    # ]
    # request_params["functions"] = [function_schema]

    # # Add OpenAI's recommended function message
    # request_params["messages"][0][
    #     "content"
    # ] += "\nUse ONLY the function you have been provided with — 'execute(language, code)'."

    ## Convert output to LMC format

    accumulated_deltas = {}
    language = None
    code = ""

    for chunk in llm.completions(**request_params):
        if "choices" not in chunk or len(chunk["choices"]) == 0:
            # This happens sometimes
            continue

        delta = chunk["choices"][0]["delta"]

        # Accumulate deltas
        accumulated_deltas = merge_deltas(accumulated_deltas, delta)

        if "content" in delta and delta["content"]:
            yield {"type": "message", "content": delta["content"]}

        if (
            accumulated_deltas.get("function_call")
            and "arguments" in accumulated_deltas["function_call"]
            and accumulated_deltas["function_call"]["arguments"]
        ):
            if (
                "name" in accumulated_deltas["function_call"]
                and accumulated_deltas["function_call"]["name"] == "execute"
            ):
                arguments = accumulated_deltas["function_call"]["arguments"]
                arguments = parse_partial_json(arguments)

                if arguments:
                    if (
                        language is None
                        and "language" in arguments
                        and "code"
                        in arguments  # <- This ensures we're *finished* typing language, as opposed to partially done
                        and arguments["language"]
                    ):
                        language = arguments["language"]

                    if language is not None and "code" in arguments:
                        # Calculate the delta (new characters only)
                        code_delta = arguments["code"][len(code) :]
                        # Update the code
                        code = arguments["code"]
                        # Yield the delta
                        if code_delta:
                            yield {
                                "type": "code",
                                "format": language,
                                "content": code_delta,
                            }
                else:
                    if llm.interpreter.verbose:
                        print("Arguments not a dict.")

            # Common hallucinations
            elif "name" in accumulated_deltas["function_call"] and (
                accumulated_deltas["function_call"]["name"] == "python"
                or accumulated_deltas["function_call"]["name"] == "functions"
            ):
                if llm.interpreter.verbose:
                    print("Got direct python call")
                if language is None:
                    language = "python"

                if language is not None:
                    # Pull the code string straight out of the "arguments" string
                    code_delta = accumulated_deltas["function_call"]["arguments"][
                        len(code) :
                    ]
                    # Update the code
                    code = accumulated_deltas["function_call"]["arguments"]
                    # Yield the delta
                    if code_delta:
                        yield {
                            "type": "code",
                            "format": language,
                            "content": code_delta,
                        }

            else:
                # If name exists and it's not "execute" or "python" or "functions", who knows what's going on.
                if "name" in accumulated_deltas["function_call"]:
                    yield {
                        "type": "code",
                        "format": "python",
                        "content": accumulated_deltas["function_call"]["name"],
                    }
                    return


def run_text_llm(llm, params):
    ## Setup

    try:
        # Add the system message
        params["messages"][0][
            "content"
        ] += "\nTo execute code on the user's machine, write a markdown code block. Specify the language after the ```. You will receive the output. Use any programming language."
    except:
        print('params["messages"][0]', params["messages"][0])
        raise

    ## Convert output to LMC format

    inside_code_block = False
    accumulated_block = ""
    language = None

    for chunk in llm.completions(**params):
        if llm.interpreter.verbose:
            print("Chunk in coding_llm", chunk)

        if "choices" not in chunk or len(chunk["choices"]) == 0:
            # This happens sometimes
            continue

        content = chunk["choices"][0]["delta"].get("content", "")

        if content == None:
            continue

        accumulated_block += content

        if accumulated_block.endswith("`"):
            # We might be writing "```" one token at a time.
            continue

        # Did we just enter a code block?
        if "```" in accumulated_block and not inside_code_block:
            inside_code_block = True
            accumulated_block = accumulated_block.split("```")[1]

        # Did we just exit a code block?
        if inside_code_block and "```" in accumulated_block:
            return

        # If we're in a code block,
        if inside_code_block:
            # If we don't have a `language`, find it
            if language is None and "\n" in accumulated_block:
                language = accumulated_block.split("\n")[0]

                # Default to python if not specified
                if language == "":
                    if llm.interpreter.os == False:
                        language = "python"
                    elif llm.interpreter.os == False:
                        # OS mode does this frequently. Takes notes with markdown code blocks
                        language = "text"
                else:
                    # Removes hallucinations containing spaces or non letters.
                    language = "".join(char for char in language if char.isalpha())

            # If we do have a `language`, send it out
            if language:
                yield {
                    "type": "code",
                    "format": language,
                    "content": content.replace(language, ""),
                }

        # If we're not in a code block, send the output as a message
        if not inside_code_block:
            yield {"type": "message", "content": content}


def display_markdown_message(message):
    """
    Display markdown message. Works with multiline strings with lots of indentation.
    Will automatically make single line > tags beautiful.
    """

    for line in message.split("\n"):
        line = line.strip()
        if line == "":
            print("")
        elif line == "---":
            rich_print(Rule(style="white"))
        else:
            try:
                rich_print(Markdown(line))
            except UnicodeEncodeError as e:
                # Replace the problematic character or handle the error as needed
                print("Error displaying line:", line)

    if "\n" not in message and message.startswith(">"):
        # Aesthetic choice. For these tags, they need a space below them
        print("")


def convert_to_openai_messages(
    messages,
    function_calling=True,
    vision=False,
    shrink_images=True,
    code_output_sender="assistant",
):
    """
    Converts LMC messages into OpenAI messages
    """
    new_messages = []

    for message in messages:
        # Is this for thine eyes?
        if "recipient" in message and message["recipient"] != "assistant":
            continue

        new_message = {}

        if message["type"] == "message":
            new_message["role"] = message[
                "role"
            ]  # This should never be `computer`, right?
            new_message["content"] = message["content"]

        elif message["type"] == "code":
            new_message["role"] = "assistant"
            if function_calling:
                new_message["function_call"] = {
                    "name": "execute",
                    "arguments": json.dumps(
                        {"language": message["format"], "code": message["content"]}
                    ),
                    # parsed_arguments isn't actually an OpenAI thing, it's an OI thing.
                    # but it's soo useful!
                    "parsed_arguments": {
                        "language": message["format"],
                        "code": message["content"],
                    },
                }
                # Add empty content to avoid error "openai.error.InvalidRequestError: 'content' is a required property - 'messages.*'"
                # especially for the OpenAI service hosted on Azure
                new_message["content"] = ""
            else:
                new_message[
                    "content"
                ] = f"""```{message["format"]}\n{message["content"]}\n```"""

        elif message["type"] == "console" and message["format"] == "output":
            if function_calling:
                new_message["role"] = "function"
                new_message["name"] = "execute"
                if message["content"].strip() == "":
                    new_message[
                        "content"
                    ] = "No output"  # I think it's best to be explicit, but we should test this.
                else:
                    new_message["content"] = message["content"]

            else:
                # This should be experimented with.
                if code_output_sender == "user":
                    if message["content"].strip() == "":
                        content = "The code above was executed on my machine. It produced no text output. what's next (if anything, or are we done?)"
                    else:
                        content = (
                            "Code output: "
                            + message["content"]
                            + "\n\nWhat does this output mean / what's next (if anything, or are we done)?"
                        )

                    new_message["role"] = "user"
                    new_message["content"] = content
                elif code_output_sender == "assistant":
                    if "@@@SEND_MESSAGE_AS_USER@@@" in message["content"]:
                        new_message["role"] = "user"
                        new_message["content"] = message["content"].replace(
                            "@@@SEND_MESSAGE_AS_USER@@@", ""
                        )
                    else:
                        new_message["role"] = "assistant"
                        new_message["content"] = (
                            "\n```output\n" + message["content"] + "\n```"
                        )

        elif message["type"] == "image":
            if vision == False:
                continue

            if "base64" in message["format"]:
                # Extract the extension from the format, default to 'png' if not specified
                if "." in message["format"]:
                    extension = message["format"].split(".")[-1]
                else:
                    extension = "png"

                # Construct the content string
                content = f"data:image/{extension};base64,{message['content']}"

                if shrink_images:
                    try:
                        # Decode the base64 image
                        img_data = base64.b64decode(message["content"])
                        img = Image.open(io.BytesIO(img_data))

                        # Resize the image if it's width is more than 1024
                        if img.width > 1024:
                            new_height = int(img.height * 1024 / img.width)
                            img = img.resize((1024, new_height))

                        # Convert the image back to base64
                        buffered = io.BytesIO()
                        img.save(buffered, format=extension)
                        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
                        content = f"data:image/{extension};base64,{img_str}"
                    except:
                        # This should be non blocking. It's not required
                        # print("Failed to shrink image. Proceeding with original image size.")
                        pass

            elif message["format"] == "path":
                # Convert to base64
                image_path = message["content"]
                file_extension = image_path.split(".")[-1]

                with open(image_path, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode("utf-8")

                content = f"data:image/{file_extension};base64,{encoded_string}"
            else:
                # Probably would be better to move this to a validation pass
                # Near core, through the whole messages object
                if "format" not in message:
                    raise Exception("Format of the image is not specified.")
                else:
                    raise Exception(f"Unrecognized image format: {message['format']}")

            # Calculate the size of the original binary data in bytes
            content_size_bytes = len(content) * 3 / 4

            # Convert the size to MB
            content_size_mb = content_size_bytes / (1024 * 1024)

            # Print the size of the content in MB
            # print(f"File size: {content_size_mb} MB")

            # Assert that the content size is under 20 MB
            assert content_size_mb < 20, "Content size exceeds 20 MB"

            new_message = {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": content, "detail": "low"},
                    }
                ],
            }

        elif message["type"] == "file":
            new_message = {"role": "user", "content": message["content"]}

        else:
            raise Exception(f"Unable to convert this message type: {message}")

        if isinstance(new_message["content"], str):
            new_message["content"] = new_message["content"].strip()

        new_messages.append(new_message)

    """
    # Combine adjacent user messages
    combined_messages = []
    i = 0
    while i < len(new_messages):
        message = new_messages[i]
        if message["role"] == "user":
            combined_content = []
            while i < len(new_messages) and new_messages[i]["role"] == "user":
                if isinstance(new_messages[i]["content"], str):
                    combined_content.append({
                        "type": "text",
                        "text": new_messages[i]["content"]
                    })
                elif isinstance(new_messages[i]["content"], list):
                    combined_content.extend(new_messages[i]["content"])
                i += 1
            message["content"] = combined_content
        combined_messages.append(message)
        i += 1
    new_messages = combined_messages

    if not function_calling:
        # Combine adjacent assistant messages, as "function calls" will just be normal messages with content: markdown code blocks
        combined_messages = []
        i = 0
        while i < len(new_messages):
            message = new_messages[i]
            if message["role"] == "assistant":
                combined_content = ""
                while i < len(new_messages) and new_messages[i]["role"] == "assistant":
                    combined_content += new_messages[i]["content"] + "\n\n"
                    i += 1
                message["content"] = combined_content.strip()
            combined_messages.append(message)
            i += 1
        new_messages = combined_messages
    """

    return new_messages


class Llm:
    """
    A stateless LMC-style LLM with some helpful properties.
    """

    def __init__(self):

        # Chat completions "endpoint"
        self.completions = fixed_litellm_completions

        # Settings
        self.model = MODEL_NAME
        self.temperature = 0
        self.supports_vision = False
        self.supports_functions = None  # Will try to auto-detect
        self.shrink_images = None

        # Optional settings
        self.context_window = None
        self.max_tokens = None
        self.api_base = BASE_URL
        self.api_key = OPENAI_API_KEY
        self.api_version = None

        # Budget manager powered by LiteLLM
        self.max_budget = None
        self.verbose = False

    def run(self, messages):
        """
        We're responsible for formatting the call into the llm.completions object,
        starting with LMC messages in interpreter.messages, going to OpenAI compatible messages into the llm,
        respecting whether it's a vision or function model, respecting its context window and max tokens, etc.

        And then processing its output, whether it's a function or non function calling model, into LMC format.
        """

        # Assertions
        assert (
            messages[0]["role"] == "system"
        ), "First message must have the role 'system'"
        for msg in messages[1:]:
            assert (
                msg["role"] != "system"
            ), "No message after the first can have the role 'system'"

        # Detect function support
        if self.supports_functions != None:
            supports_functions = self.supports_functions
        else:
            # Guess whether or not it's a function calling LLM
            # Once Litellm supports it, add Anthropic models here
            if self.model != "gpt-4-vision-preview" and self.model in litellm.open_ai_chat_completion_models or self.model.startswith("azure/"):
                supports_functions = True
            else:
                supports_functions = False

        # Trim image messages if they're there
        if self.supports_vision:
            image_messages = [msg for msg in messages if msg["type"] == "image"]

            if self.interpreter.os:
                # Keep only the last two images if the interpreter is running in OS mode
                if len(image_messages) > 1:
                    for img_msg in image_messages[:-2]:
                        messages.remove(img_msg)
                        if self.interpreter.verbose:
                            print("Removing image message!")
            else:
                # Delete all the middle ones (leave only the first and last 2 images) from messages_for_llm
                if len(image_messages) > 3:
                    for img_msg in image_messages[1:-2]:
                        messages.remove(img_msg)
                        if self.interpreter.verbose:
                            print("Removing image message!")
                # Idea: we could set detail: low for the middle messages, instead of deleting them

        # Convert to OpenAI messages format
        # messages = convert_to_openai_messages(
        #     messages,
        #     function_calling=supports_functions,
        #     vision=self.supports_vision,
        #     shrink_images=self.shrink_images,
        # )

        # if self.interpreter.debug:
        #     print("\n\n\nOPENAI COMPATIBLE MESSAGES\n\n\n")
        #     for message in messages:
        #         if len(str(message)) > 5000:
        #             print(str(message)[:200] + "...")
        #         else:
        #             print(message)
        #         print("\n")
        #     print("\n\n\n")

        system_message = messages[0]["content"]
        messages = messages[1:]

        # Trim messages
        try:
            if self.context_window and self.max_tokens:
                trim_to_be_this_many_tokens = (
                    self.context_window - self.max_tokens - 25
                )  # arbitrary buffer
                messages = tt.trim(
                    messages,
                    system_message=system_message,
                    max_tokens=trim_to_be_this_many_tokens,
                )
            elif self.context_window and not self.max_tokens:
                # Just trim to the context window if max_tokens not set
                messages = tt.trim(
                    messages,
                    system_message=system_message,
                    max_tokens=self.context_window,
                )
            else:
                try:
                    messages = tt.trim(
                        messages, system_message=system_message, model=self.model
                    )
                except:
                    if len(messages) == 1:
                        if self.interpreter.in_terminal_interface:
                            display_markdown_message(
                                """
**We were unable to determine the context window of this model.** Defaulting to 3000.

If your model can handle more, run `interpreter --context_window {token limit} --max_tokens {max tokens per response}`.

Continuing...
                            """
                            )
                        else:
                            display_markdown_message(
                                """
**We were unable to determine the context window of this model.** Defaulting to 3000.

If your model can handle more, run `interpreter.llm.context_window = {token limit}`.

Also please set `interpreter.llm.max_tokens = {max tokens per response}`.

Continuing...
                            """
                            )
                    messages = tt.trim(
                        messages, system_message=system_message, max_tokens=3000
                    )
        except:
            # If we're trimming messages, this won't work.
            # If we're trimming from a model we don't know, this won't work.
            # Better not to fail until `messages` is too big, just for frustrations sake, I suppose.

            # Reunite system message with messages
            messages = [{"role": "system", "content": system_message}] + messages

            pass

        ## Start forming the request

        params = {
            "model": self.model,
            "messages": messages,
            "stream": True,
        }

        # Optional inputs
        if self.api_key:
            params["api_key"] = self.api_key
        if self.api_base:
            params["api_base"] = self.api_base
        if self.api_version:
            params["api_version"] = self.api_version
        if self.max_tokens:
            params["max_tokens"] = self.max_tokens
        if self.temperature:
            params["temperature"] = self.temperature

        # Set some params directly on LiteLLM
        if self.max_budget:
            litellm.max_budget = self.max_budget
        if self.verbose:
            litellm.set_verbose = True

        if supports_functions:
            yield from run_function_calling_llm(self, params)
        else:
            yield from run_text_llm(self, params)


def fixed_litellm_completions(**params):
    """
    Just uses a dummy API key, since we use litellm without an API key sometimes.
    Hopefully they will fix this!
    """

    # Run completion
    first_error = None
    try:
        yield from litellm.completion(**params)
    except Exception as e:
        # Store the first error
        first_error = e
        # LiteLLM can fail if there's no API key,
        # even though some models (like local ones) don't require it.

        if "api key" in str(first_error).lower() and "api_key" not in params:
            print(
                "LiteLLM requires an API key. Please set a dummy API key to prevent this message. (e.g `interpreter --api_key x` or `interpreter.llm.api_key = 'x'`)"
            )

        # So, let's try one more time with a dummy API key:
        params["api_key"] = "x"

        try:
            yield from litellm.completion(**params)
        except:
            # If the second attempt also fails, raise the first error
            raise first_error


def main():
    start_time = time.time()
    llm = Llm()
    # query = '你好，请随便和我说点什么'
    messages = [{'role': 'system', 'content': 'You are Open Interpreter, a world-class programmer that can complete any goal by executing code.\nFirst, write a plan. **Always recap the plan between each code block** (you have extreme short-term memory loss, so you need to recap the plan between each message block to retain it).\nWhen you execute code, it will be executed **on the user\'s machine**. The user has given you **full and complete permission** to execute any code necessary to complete the task. Execute the code.\nIf you want to send data between programming languages, save the data to a txt or json.\nYou can access the internet. Run **any code** to achieve the goal, and if at first you don\'t succeed, try again and again.\nYou can install new packages.\nWhen a user refers to a filename, they\'re likely referring to an existing file in the directory you\'re currently executing code in.\nWrite messages to the user in Markdown.\nIn general, try to **make plans** with as few steps as possible. As for actually executing code to carry out that plan, for *stateful* languages (like python, javascript, shell, but NOT for html which starts from 0 every time) **it\'s critical not to try to do everything in one code block.** You should try something, print information about it, then continue from there in tiny, informed steps. You will never get it on the first try, and attempting it in one go will often lead to errors you cant see.\nYou are capable of **any** task.\n\n# THE COMPUTER API\n\nA python `computer` module is ALREADY IMPORTED, and can be used for many tasks:\n\n```python\ncomputer.browser.search(query) # Google search results will be returned from this function as a string\ncomputer.files.edit(path_to_file, original_text, replacement_text) # Edit a file\ncomputer.calendar.create_event(title="Meeting", start_date=datetime.datetime.now(), end=datetime.datetime.now() + datetime.timedelta(hours=1), notes="Note", location="") # Creates a calendar event\ncomputer.calendar.get_events(start_date=datetime.date.today(), end_date=None) # Get events between dates. If end_date is None, only gets events for start_date\ncomputer.calendar.delete_event(event_title="Meeting", start_date=datetime.datetime) # Delete a specific event with a matching title and start date, you may need to get use get_events() to find the specific event object first\ncomputer.contacts.get_phone_number("John Doe")\ncomputer.contacts.get_email_address("John Doe")\ncomputer.mail.send("john@email.com", "Meeting Reminder", "Reminder that our meeting is at 3pm today.", ["path/to/attachment.pdf", "path/to/attachment2.pdf"]) # Send an email with a optional attachments\ncomputer.mail.get(4, unread=True) # Returns the {number} of unread emails, or all emails if False is passed\ncomputer.mail.unread_count() # Returns the number of unread emails\ncomputer.sms.send("555-123-4567", "Hello from the computer!") # Send a text message. MUST be a phone number, so use computer.contacts.get_phone_number frequently here\n```\n\nDo not import the computer module, or any of its sub-modules. They are already imported.\n\nUser InfoName: hanchengcheng\nCWD: /Users/hanchengcheng/Documents/official_space/open-interpreter\nSHELL: /bin/bash\nOS: Darwin\nUse ONLY the function you have been provided with — \'execute(language, code)\'.'}, {'role': 'user', 'content': "Plot AAPL and META's normalized stock prices"}]
    # functions = {'name': 'execute', 'description': "Executes code on the user's machine **in the users local environment** and returns the output", 'parameters': {'type': 'object', 'properties': {'language': {'type': 'string', 'description': 'The programming language (required parameter to the `execute` function)', 'enum': ['ruby', 'python', 'shell', 'javascript', 'html', 'applescript', 'r', 'powershell', 'react']}, 'code': {'type': 'string', 'description': 'The code to execute (required)'}}, 'required': ['language', 'code']}}
    # request_params = {'model': 'gpt-4-0125-preview', 'messages': messages, 'stream': True, 'api_key': 'sk-RoqgGFXo94mScVAo8aFdC3Ec36E14eFbAeE0D72f9437292a', 'api_base': 'https://api.chatweb.plus/v1', 'functions': [functions]}
    response = ''
    for output in llm.run(messages):
        response += output['content']
        # print(output)
    print(response)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"生成的单词数: {len(response)}")
    print(f"程序执行时间: {execution_time}秒")

if __name__ == '__main__':
    main()