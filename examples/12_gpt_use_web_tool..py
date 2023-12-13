import langchain
from langchain.chains import Chain
from langchain.prompts import SimplePrompt
from langchain.components import OpenAI, WebSearch

# 创建 ChatGPT 和 Bing API 组件
chatgpt = OpenAI(api_key='your_openai_api_key')
bing_api = WebSearch(api_key='your_bing_api_key')

# 定义一个链式流程
chain = Chain(components=[chatgpt, bing_api])

# 定义一个提示
prompt = SimplePrompt(prompt="What is the capital of France?")

# 执行链式流程
result = chain.run(prompt)

print(result)
