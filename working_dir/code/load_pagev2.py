from jarvis.core.tool_request_util import ToolRequestUtil

# Initialize the ToolRequestUtil
tool_request_util = ToolRequestUtil()

# Extract the URL for the lyrics page from the context
lyrics_page_url = "https://genius.com/Michael-jackson-human-nature-lyrics"  # URL from the first search result

# Set up the parameters for the API call
api_path = '/tools/bing/load_pagev2'
method = 'get'
params = {
    "url": lyrics_page_url,
    "query": "Michael Jackson – Human Nature Lyrics"
}

# Call the API
response = tool_request_util.request(api_path, method, params=params, content_type='application/json')

# Print the return value of the API
print(response)