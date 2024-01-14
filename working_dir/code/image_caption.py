from jarvis.core.tool_request_util import ToolRequestUtil

from jarvis.core.tool_request_util import ToolRequestUtil

# Initialize the ToolRequestUtil
tool_request_util = ToolRequestUtil()

# Define the API path
api_path = '/tools/image_caption'

# Define the method to be used for the API call
method = 'post'

# Define the query parameter to specify the task of extracting butterfat content information
query_params = {'query': 'What brand are the harnesses the dogs are wearing?'}

# Define the file to be uploaded
file_path = '/home/heroding/.cache/huggingface/datasets/downloads/931dbe038478709e8d21e5d04703e9855f590061682b778b9612067c117cdb37.jpg'
files = {'image_file': open(file_path, 'rb')}

# Make the API call using the ToolRequestUtil
response = tool_request_util.request(api_path, method, params=query_params, files=files, content_type='multipart/form-data')

# Close the file after the request is made
files['image_file'].close()

# Print the return value of the API call
print(response)