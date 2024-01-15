from jarvis.core.tool_request_util import ToolRequestUtil

# Initialize the ToolRequestUtil
tool_request_util = ToolRequestUtil()

# Define the API path
api_path = '/tools/bing/searchv2'

# Define the method to be used for the API request
method = 'get'

# Define the parameters for the API request
# The query is constructed to include information about koi fish, the watershed id, and the year
params = {
    "query": "koi fish 02040203",
    "top_k": None  # Assuming we want the default number of results
}

# Define the content type for the API request
content_type = 'application/json'

# Make the API request and store the response
response = tool_request_util.request(api_path, method, params=params, content_type=content_type)

# Print the response from the API
print(response)