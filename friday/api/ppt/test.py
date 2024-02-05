import requests

ppt_url='http://localhost:8079/tools/ppt'

#创建文件
requests.post(f'{ppt_url}/create_file', json={"theme": "tech"})
#获取图片
response = requests.post(f'{ppt_url}/get_image', json={"keywords": "programming"})
image_path = response.json()
#加一页
requests.post(f'{ppt_url}/add_first_page', json={"title": "About Me", "subtitle": "A brief introduction"})
requests.post(f'{ppt_url}/add_text_page', json={"title": "Education", "bullet_items": "Bachelor's Degree in Computer Science[SPAN]Master's Degree in Data Science"})
requests.post(f'{ppt_url}/add_text_image_page', json={"title": "Skills", "bullet_items": "Programming[SPAN]Data Analysis[SPAN]Machine Learning", "image": image_path})
response = requests.get(f'{ppt_url}/submit_file')
file_path = response.json()
print(file_path)