from langchain.tools import BaseTool, StructuredTool, Tool, tool
from jarvis.core.web_browser import web_browser
from langchain.utilities import BingSearchAPIWrapper
from jarvis.core.tools_args_schema import *
import os
os.environ["BING_SUBSCRIPTION_KEY"] = "885e62a126554fb390af88ae31d2c8ff"
os.environ["BING_SEARCH_URL"] = "https://api.bing.microsoft.com/v7.0/search"

def bing_search_func(query,top_k=5):
    search = BingSearchAPIWrapper()
    return search.results(query,top_k)

web_browser_tool = Tool(
    name="web_browser",
    description="You can use this tool to browser the detail content of the web page given its url",
    func=web_browser,
    args_schema = WebBrowserInput
    
)

# class BingSearchTool(BaseTool):
#     name = "bing_search"
#     description:str ="You can use this tool to search top 10 relevant web pages' link and very short description for the given query keywords.You sometimes need to use web browser to get detailed information of some page",
 
#     def _run(self, query: str, top_k: int=5) -> str:
#         """使用工具。"""
#         search = BingSearchAPIWrapper()
#         return search.results(query,top_k)
    
#     async def _arun(self, query: str) -> str:
#         """异步使用工具。"""
#         raise NotImplementedError("BingSearchTool不支持异步")
# bing_search_tool = BingSearchTool()
bing_search_tool = Tool(
    name="bing_search",
    description="You can use this tool to search top 10 relevant web pages' link and very short description for the given query keywords.You sometimes need to use web browser to get detailed information of some page",
    func=bing_search_func,
    args_schema = BingSearchInput
)

test_tool = Tool(
    name="test",
    description="You can use this tool to test the tool agent",
    func= lambda a,b : "",
    # args_schema = TestInput

)

res = test_tool(1,2)
# print(res)

tools_dict = {
    "bing_search": bing_search_tool,
    "web_browser": web_browser_tool
}
