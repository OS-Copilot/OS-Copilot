# from openai import OpenAI
# import os
# os.environ["OPENAI_API_KEY"] = "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"
# os.environ["OPENAI_ORGANIZATION"] = "org-fSyygvftM73W0pK4VjoK395W"
# client = OpenAI()

# response = client.chat.completions.create(
#   model="gpt-4-vision-preview",
#   messages=[
#     {
#       "role": "user",
#       "content": [
#         {"type": "text", "text": "Can you explain the formula in the picture for me?"},
#         {
#           "type": "image_url",
#           "image_url": {
#             "url": "https://dasex101-random-learning.oss-cn-shanghai.aliyuncs.com/forma.png",
#           },
#         },
#       ],
#     }
#   ],
#   max_tokens=300,
# )

# print(response.choices[0])