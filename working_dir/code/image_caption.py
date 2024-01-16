from jarvis.core.tool_request_util import ToolRequestUtil

from jarvis.core.tool_request_util import ToolRequestUtil

# Initialize the ToolRequestUtil
tool_request_util = ToolRequestUtil()

# Define the API path
api_path = '/tools/image_caption'

# Define the method to be used for the API call
method = 'post'

# Define the query parameter to specify the task of extracting butterfat content information
query_params = {'query': 'How many cats are in the attached photo, including those that are partially obscured or not fully in frame?'}

# Define the file to be uploaded
file_path = '/home/heroding/.cache/huggingface/datasets/downloads/28242018ceba2e5429c7fa9fe177fc248eed4d3e90b266190c0175a97166f20b.jpg'
files = {'image_file': open(file_path, 'rb')}

# Make the API call using the ToolRequestUtil
response = tool_request_util.request(api_path, method, params=query_params, files=files, content_type='multipart/form-data')

# Close the file after the request is made
files['image_file'].close()

# Print the return value of the API call
print(response)