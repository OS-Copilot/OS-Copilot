from langchain import OpenAI, PromptTemplate, LLMChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.mapreduce import MapReduceChain
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
 
import json
with open("../../examples/config.json") as f:
    config = json.load(f) 
llm = OpenAI(
    temperature=0,
    openai_api_key=config['OPENAI_API_KEY'],
    openai_organization=config['OPENAI_ORGANIZATION'],
    # model_name="gpt-3.5-turbo-1106"
    )
 
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=30)
with open('./test.txt') as f:
    state_of_the_union = f.read()
texts = text_splitter.create_documents([state_of_the_union])
chain = load_summarize_chain(llm, chain_type="map_reduce")
res = chain.run(texts)
print(res)

