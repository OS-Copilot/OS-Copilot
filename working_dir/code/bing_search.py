from jarvis.core.tool_request_util import ToolRequestUtil

# Initialize the ToolRequestUtil
tool_request_util = ToolRequestUtil()

# Define the API path
api_path = '/tools/bing/load_pagev2'

# Define the method to be used for the API request
method = 'get'

# Based on the context provided, the URL for the Lego 4855 instruction manual is obtained from the previous search
url = "https://www.lego.com/en-us/service/buildinginstructions"

# Define the query for the API request
query = ''

# Define the params for the API request
params = {
    'url': url,
    'query': query
}

# Define the content type for the API request
content_type = 'application/json'

# Make the API request and store the response
response = tool_request_util.request(api_path, method, params=params, content_type=content_type)

# Print the return value of the API
print(response)