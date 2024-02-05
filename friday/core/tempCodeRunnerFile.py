files = {'file': open("test.mp3", "rb")}

res = requests.post(url,
                   headers=headers,
                   files=files,
                     timeout=30)
