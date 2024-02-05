from friday.core.tool_request_util import ToolRequestUtil

# Initialize the ToolRequestUtil
tool_request_util = ToolRequestUtil()

# Define the API path
api_path = "/tools/bing/load_pagev2"

# Define the method to be used for the API call
method = "get"

# Define the parameters for the API call
params = {
    "query": "Vietnamese specimens described by Kuznetzov in Nedoshivina's 2010 paper deposition",
    "url": "https://www.zobodat.at/pdf/Atalanta_41_0335-0347.pdf"  # We only need the top result since we are looking for a specific piece of information
}

# Define the content type
content_type = "application/json"

# Make the API call and store the response
response = tool_request_util.request(api_path, method, params=params, content_type=content_type)

# Print the return value of the API call
print(response)