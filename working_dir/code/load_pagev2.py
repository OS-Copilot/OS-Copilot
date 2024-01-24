from jarvis.core.tool_request_util import ToolRequestUtil

# Initialize the ToolRequestUtil
tool_request_util = ToolRequestUtil()

# Define the API path
api_path = '/tools/bing/load_pagev2'

# Define the method for the API call
method = 'get'

# Extract the URL from the previous task's context
bls_page_url = "https://www.bls.gov/news.release/archives/empsit_07022009.pdf"

# Define the query for the API call
query = ''

# Define the params for the API call
params = {
    'url': bls_page_url,
    'query': query
}

# Define the content type
content_type = 'application/json'

# Make the API call and print the return value
response = tool_request_util.request(api_path, method, params=params, content_type=content_type)
print(response)