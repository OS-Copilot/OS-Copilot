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
file_path = '/home/heroding/.cache/huggingface/datasets/downloads/30628ff4e5650083191b5763452662b2c0818a8ca2daef455a91860cc34ef490.mp3'
files = {'file': ('audio.mp3', open(file_path, 'rb'))}

# Make the API request and get the response
response = tool_request_util.request(api_path=api_path, method=method, params=params, files=files, content_type=content_type)

# Print the response from the API
print(response)