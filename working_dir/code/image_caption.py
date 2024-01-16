from jarvis.core.tool_request_util import ToolRequestUtil

from jarvis.core.tool_request_util import ToolRequestUtil

# Initialize the ToolRequestUtil
tool_request_util = ToolRequestUtil()

# Define the API path
api_path = '/tools/image_caption'

# Define the method to be used for the API call
method = 'post'

# Define the query parameter to specify the task of extracting butterfat content information
query_params = {'query': 'As a comma separated list with no whitespace, using the provided image provide all the fractions that use / as the fraction line and the answers to the sample problems. Order the list by the order in which the fractions appear.'}

# Define the file to be uploaded
file_path = '/home/heroding/.cache/huggingface/datasets/downloads/2105d7660150b62c9b52b778082c3ba8bd69ecc463e61343dbf0f6e79c96294a.png'
files = {'image_file': open(file_path, 'rb')}

# Make the API call using the ToolRequestUtil
response = tool_request_util.request(api_path, method, params=query_params, files=files, content_type='multipart/form-data')

# Close the file after the request is made
files['image_file'].close()

# Print the return value of the API call
print(response)