from jarvis.core.tool_request_util import ToolRequestUtil

# Initialize the ToolRequestUtil
tool_request_util = ToolRequestUtil()

# Define the API path and method
api_path = "/tools/bing/searchv2"
method = "get"

# Define the query parameters
params = {
    "query": "Mercedes Sosa studio albums 2000-2009",
    "top_k": 1  # We only need the top result since we're looking for a specific Wikipedia page
}

# Make the API request
response = tool_request_util.request(api_path, method, params=params, content_type="application/json")

# Print the response from the API
print(response)