from langchain.agents import load_tools  
from langchain.agents import initialize_agent  
from langchain.agents import AgentType  
from langchain.llms import OpenAI  
import os 
os.environ[ "OPENAI_API_KEY" ] = "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"
os.environ[ "OPENAI_ORGANIZATION" ] = "org-fSyygvftM73W0pK4VjoK395W"
os.environ[ "model_name" ] = "gpt-3.5-turbo-1106"
os.environ["BING_SUBSCRIPTION_KEY"] = "885e62a126554fb390af88ae31d2c8ff"
os.environ["BING_SEARCH_URL"] = "https://api.bing.microsoft.com/v7.0/search"
# First, let's load the language model we're going to use to control the agent.  
llm = OpenAI(temperature=0)  
  
# Next, let's load some tools to use. Note that the `llm-math` tool uses an LLM, so we need to pass that in.  
tools = load_tools(["bing-search"], llm=llm)
  
  
# Finally, let's initialize an agent with the tools, the language model, and the type of agent we want to use.  
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)  
  
# Now let's test it out!  
agent.run("介绍一下gpt-4.5-turbo")