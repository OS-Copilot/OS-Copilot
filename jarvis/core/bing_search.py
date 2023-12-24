from jarvis.core.tool_request_util import ToolRequestUtil

# Initialize the ToolRequestUtil
tool_request_util = ToolRequestUtil()

# Define the API path
api_path = "/tools/bing/searchv2"

# Define the method to be used for the API call
method = "get"

# Define the parameters for the API call
params = {
    "query": "Mercedes Sosa studio albums 2000-2009 site:en.wikipedia.org",
    "top_k": 5  # We only need the top result since we are looking for a specific piece of information
}

# Define the content type
content_type = "application/json"

# Make the API call and store the response
response = tool_request_util.request(api_path, method, params=params, content_type=content_type)

# Print the return value of the API call
print(response)