from jarvis.core.tool_request_util import ToolRequestUtil

# Initialize the ToolRequestUtil
tool_request_util = ToolRequestUtil()

# Define the API path and the method to be used
api_path = '/tools/bing/image_search'
method = 'get'

# Define the parameters for the API call
params = {
    "query": "East China Normal University",
    "top_k": 3
}

# Define the content type
content_type = 'application/json'

# Make the API call using the ToolRequestUtil
response = tool_request_util.request(api_path, method, params=params, content_type=content_type)

# Print the return value of the API call
print(response)