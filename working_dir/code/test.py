from jarvis.core.tool_request_util import ToolRequestUtil

# Initialize the ToolRequestUtil
tool_request_util = ToolRequestUtil()

# Extract the URL from the context provided
research_article_url = "https://www.science.org/doi/10.1126/sciadv.abi8620"

# Construct the query to find the most relevant content about the age of the beads
query = "abstract"

# Prepare the parameters for the API call
params = {
    "url": research_article_url,
    "query": query
}

# Call the '/tools/bing/load_pagev2' API using the ToolRequestUtil
response = tool_request_util.request(api_path="/tools/bing/load_pagev2", method="get", params=params)

# Print the return value of the API
print(response)