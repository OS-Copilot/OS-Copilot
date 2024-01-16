from jarvis.core.tool_request_util import ToolRequestUtil

# Initialize the ToolRequestUtil
tool_request_util = ToolRequestUtil()

# Extract the URL for the lyrics page from the context
lyrics_page_url = "https://www.fao.org/3/ca8753en/ca8753en.pdf"  # URL from the first search result

# Set up the parameters for the API call
api_path = '/tools/bing/load_pagev2'
method = 'get'
params = {
    "url": lyrics_page_url,
    "query": ""
}

# Call the API
response = tool_request_util.request(api_path, method, params=params, content_type='application/json')

# Print the return value of the API
print(response)