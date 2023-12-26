from jarvis.core.llms import OpenAI
import json
QA_SYS_PROMPT='''
You are a helpful ai assistant that can answer the questions asked by the user
with the help of the context provided by the user in a step by step manner.
If you don't know how to answer the user's question, answer "I don't know how to answer" instead of making up an answer.
'''
QA_USER_PROMPT='''
context: {context}
question: {question}
'''
class AnswerAgent():
    ''' Answer is used to answer the question asked by the user'''
    def __init__(self, config_path=None, open_api_doc_path = None) -> None:
        super().__init__()
        self.llm = OpenAI(config_path)

        # self.mac_systom_prompts = 

    def generate_call_api_code(self, question,context="No context provided."):
        self.sys_prompt = QA_SYS_PROMPT
        self.user_prompt = QA_USER_PROMPT.format(
            question = question,
            context = context
        )
        self.message = [
            {"role": "system", "content": self.sys_prompt},
            {"role": "user", "content": self.user_prompt},
        ]
        return self.llm.chat(self.message)
  