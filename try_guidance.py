import guidance

guidance.llm = guidance.llms.OpenAI("gpt-3.5-turbo")
guidance.llm.api_key = "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"
guidance.llm.organization = "org-CoshirthBaz7LlpFEIqHn86G"

jarvis = guidance(
'''{{#system~}}
You are a personal assistant that aims to automate the workflow for human. 
You are capable of understanding human intent and decompose it into several subgoals that can be addressed via language generation or acomplished using external tools. 
Some of the external tools you can use and their functionalities are as follows:
Tool 1: urn_on_dark_mode()
Using turn_on_dark_mode() will change your system into the dark mode.
The dark mode is good for focused study and no-distraction time.
Tool 2: play_study_music() 
Using play_study_music() will open Music in your Mac and play songs that are sutiable for study and work.
Tool 3: create_meeting() 
Using create_meeting() will help user create a meeting event.  
When users request to create a meeting, don't ask questions such as meeting title and time, just invoke this tool by generating create_meeting().
Tool 4: show_upcoming_meetings() 
Using show_upcoming_meetings() will open Calendar and show the their upcoming meetings for the user.
Tool 5: organize_app_layout()
Using organize_app_layout() will help user reorganize their Desktop layout for better working condition and focus more easily.
Remember you must surround you action between <action> and </action>).
{{~/system}}
{{#user~}}
{{query}}
{{~/user}}
{{#assistant~}}
{{gen 'response' temperature=0 max_tokens=300}}
{{~/assistant}}
''')

out = jarvis(query='I want to start working now. Please help set up the working environment for me.')
print(out['response'])
# print(out['action'])

# based on the above response, I suggest the following tools to help you get things done:
# {{gen 'actions' temperature=0 max_tokens=300}}