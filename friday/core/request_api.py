from friday.core.tool_request_util import ToolRequestUtil

# Initialize the ToolRequestUtil
tool_request_util = ToolRequestUtil()

# Define the API path
api_path = '/tools/bing/load_pagev2'

# Define the method to be used for the API call
method = 'get'

# Extract the search results from the 'internet_search' subtask context
search_results = [
    {
        "snippet": "Abstract: 67 species described by V. Kuznetzov from Vietnam are listed with short comments on the type series including descrip-tions of their labels. Colour images of the holotypes are given (col. pl. 7-9). Descriptions of †† of five species are provided and their genitalia are figured.",
        "title": "A catalogue of type specimens of the Tortricidae described by V. I. K ...",
        "link": "https://www.zobodat.at/pdf/Atalanta_41_0335-0347.pdf"
    },
    # ... other search results
]

# Define the query parameter based on the task description
query = "Vietnamese specimens described by Kuznetzov in Nedoshivina's 2010 paper deposition"

# Since the API requires a URL, we will use the first link from the search results
url = search_results[0]['link']
print(url)
# Prepare the params for the API call
params = {
    'url': url,
    'query': query
}

# Make the API call using the ToolRequestUtil
response = tool_request_util.request(api_path, method, params=params)

# Print the return value of the API
print(response)