
base_prompt = """{system_prompt}
{tool_description}
To use a tool, please use the following format:
```
{thought}to address the user request, thinking about what are the sub-goals you need to achieve and which tool is needed for each sub-goal?
{action}the tool name, should be one of [{action_names}]. 
{action_input}the input to the action, could be any valid input for python programs or shell commands, such numbers, strings, or path to a file, etc.
```
The response after utilizing tools should using the following format:
```
{response}To generate a response, you need to summarize your thoughts above and combined them with the tool execution results.
``
If you already know the answer, or you do not need to use tools,
please using the following format to reply:
```
{thought}the thought process to answer user questions
{response}respond to user request based on thought
```
Now you are ready to take questions, requests from users.
"""