from openai import OpenAI

class ImageCaptionTool:
    def __init__(self) -> None:
        self.client = OpenAI()
    def caption(self,url,query="What's in this Image?"):
        response = self.client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
            "role": "user",
            "content": [
                {"type": "text", "text": query},
                {
                "type": "image_url",
                "image_url": {
                    "url": url,
                },
                },
            ],
            }
        ],
        max_tokens=300,
        )
        return response.choices[0].message.content
    

# tool = ImageCaptionTool()
# import base64
# # Function to encode the image
# def encode_image(image_path):
#   with open(image_path, "rb") as image_file:
#     return base64.b64encode(image_file.read()).decode('utf-8')
# # Path to your image
# image_path = "birds.jpg"

# # Getting the base64 string
# base64_image = encode_image(image_path)
# res = tool.caption(url=f"data:image/jpeg;base64,{base64_image}")
# print(res)