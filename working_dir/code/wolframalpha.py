from jarvis.core.tool_request_util import ToolRequestUtil

# Initialize the ToolRequestUtil
tool_request_util = ToolRequestUtil()

# The Tropicos ID extracted from the context
tropicos_id = "100370510"

# Formulate the query to calculate the ISBN-10 check digit for the Tropicos ID
query = f"100^100000"

# Prepare the request body according to the API documentation
request_body = {
    "query": query
}

# Call the API using the ToolRequestUtil
response = tool_request_util.request(
    api_path="/tools/wolframalpha",
    method="post",
    params=request_body,
    content_type="application/json"
)

# Print the return value of the API
print(response)