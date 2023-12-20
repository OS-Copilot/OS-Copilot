from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader
import json
with open("../../examples/config.json") as f:
    config = json.load(f)
with open('./test.txt') as f:
    state_of_the_union = f.read()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
texts = text_splitter.create_documents([state_of_the_union])

embeddings = OpenAIEmbeddings(
    openai_api_key=config['OPENAI_API_KEY'],
    openai_organization=config['OPENAI_ORGANIZATION'],
)
docsearch = Chroma.from_documents(texts, embeddings)
query = "请总结https://zhuanlan.zhihu.com/p/541484549这个网页主要讲了什么"
docs = docsearch.similarity_search(query, k=5)
res = '...'.join([doc.page_content for doc in docs])
print(res)