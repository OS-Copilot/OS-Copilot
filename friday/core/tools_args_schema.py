from pydantic import BaseModel,Field
class WebBrowserInput(BaseModel):
    url: str = Field(..., description="The url to load")
    max_retry: int = Field(3, description="The max retry times to load the url")
class BingSearchInput(BaseModel):
    query: str = Field(..., description="The query keywords for bing search")
    top_k: int = Field(5, description="The number of top k results to return")
class TestInput(BaseModel):
    a: int = Field(..., description="The first number")
    b: int = Field(..., description="The second number")