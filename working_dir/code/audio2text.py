from jarvis.core.tool_request_util import ToolRequestUtil

# Initialize the ToolRequestUtil
tool_request_util = ToolRequestUtil()

# Define the API path
api_path = '/tools/audio2text'

# Define the method to be used for the request
method = 'post'

# Since the API documentation does not specify any additional parameters, we will set params to None
params = None

# Set the content type for the request
content_type = 'multipart/form-data'

# Specify the file path and the file parameter name as per the API documentation
file_path = '/home/heroding/.cache/huggingface/datasets/downloads/34e97eca75c3502bb3aeb467b74c4239a5a3afcfdfb8becb223d3327c235ec6f.mp3'
files = {'file': ('audio.mp3', open(file_path, 'rb'))}

# Make the API request and get the response
response = tool_request_util.request(api_path=api_path, method=method, params=params, files=files, content_type=content_type)

# Print the response from the API
print(response)