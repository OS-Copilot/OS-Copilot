from jarvis.core.tool_request_util import ToolRequestUtil

from jarvis.core.tool_request_util import ToolRequestUtil

# Initialize the ToolRequestUtil
tool_request_util = ToolRequestUtil()

# Define the API path
api_path = '/tools/image_caption'

# Define the method to be used for the API call
method = 'post'

# Define the query parameter to specify the task of extracting butterfat content information
query_params = {'query': 'The opponent of the player who has the grid in the attached image file calls out the first move made in Game 10 of the World Chess Championship title match won by Bobby Fischer, using algebraic notation. What is the name of the game piece into which the player will have to put a red peg as a result, according to the 1990 Milton Bradley rules for the game? Answer without articles.'}

# Define the file to be uploaded
file_path = '/home/heroding/.cache/huggingface/datasets/downloads/ed21e60f7812244ba022e33c79b47baeeb30c332753afa4a0d0b01fdca48763b.png'
files = {'image_file': open(file_path, 'rb')}

# Make the API call using the ToolRequestUtil
response = tool_request_util.request(api_path, method, params=query_params, files=files, content_type='multipart/form-data')

# Close the file after the request is made
files['image_file'].close()

# Print the return value of the API call
print(response)