from jarvis.core.tool_request_util import ToolRequestUtil

# Initialize the ToolRequestUtil
tool_request_util = ToolRequestUtil()

# Define the API path
api_path = '/tools/image_caption'

# Define the method to use for the API call
method = 'post'

# Define the query parameter as specified by the user
params = {'query': 'What is the area of the green polygon in the attached file? The numbers in purple represent the lengths of the side they are next to.'}

# Define the file to be uploaded
image_file_path = '/home/heroding/.cache/huggingface/datasets/downloads/4dfb58b43940b583e06b57d399c6bf419a9e5927fd5728dd43baed17bc1dd187.png'
files = {'image_file': open(image_file_path, 'rb')}

# Define the content type for the API call
content_type = 'multipart/form-data'

# Make the API call and get the response
response = tool_request_util.request(api_path=api_path, method=method, params=params, files=files, content_type=content_type)

# Close the file after the request is made
files['image_file'].close()

# Print the return value of the API
print(response)