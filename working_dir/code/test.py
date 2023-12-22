# import json

# dict =         {
#             'retrieve_files' : {
#                 'name': 'retrieve_files',
#                 'description': 'retrieve the txt text in the folder call document in the working directory. If the text contains the word "agent", save the path of the text file into the list, and return.',
#                 'dependencies': []
#             },
#             'organize_files' : {
#                 'name': 'organize_files',
#                 'description': 'put the retrieved files into a folder named agent based on the file path list obtained by executing the previous task.',
#                 'dependencies': ['retrieve_files']
#             }    
#         } 

# print(json.dumps(dict))