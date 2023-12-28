from jarvis.core.tool_request_util import ToolRequestUtil

api_path = "/tools/bing/searchv2"

# Define the method
method = "get"

# Define the parameters
params = {
    "query": "GitHub blog of Zhiyong Wu from Shanghai AI Lab",
    "top_k": 5
}

# Define the content type
content_type = "application/json"

# Make the request
response = ToolRequestUtil().request(api_path, method, params, content_type)

# Print the response
print(response)