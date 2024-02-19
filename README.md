# OS-Copilot: Towards Generalist Computer Agents with Self-Improvement

<div align="center">

[[Website]](https://os-copilot.github.io/)
[[Arxiv]](https://arxiv.org/abs/2402.07456)
[[PDF]](https://arxiv.org/pdf/2402.07456.pdf)
<!-- [[Tweet]](https://twitter.com/DrJimFan/status/1662115266933972993?s=20) -->

[![Static Badge](https://img.shields.io/badge/MIT-License-green)](https://github.com/OS-Copilot/FRIDAY/blob/main/LICENSE)
![Static Badge](https://img.shields.io/badge/python-3.10-blue)
[![Static Badge](https://img.shields.io/badge/FRIDAY-Frontend-yellow)](https://github.com/OS-Copilot/FRIDAY-front)



<p align="center">
  <img src='pic/demo.png' width="100%">
</p>

</div>

## 📖 Overview

- **OS-Copilot** is a pioneering conceptual framework for building generalist computer agents on Linux and MacOS, which provides a unified interface for app interactions in the heterogeneous OS ecosystem.
  
<p align="center">
  <img src='pic/framework.png' width="75%">
</p>

- Leveraging OS-Copilot, we built **FRIDAY**, a self-improving AI assistant capable of solving general computer tasks.

<p align="center">
  <img src='pic/FRIDAY.png' width="75%">
</p>

## ⚡️ Quickstart

1. **Clone the GitHub Repository:** 

   ```
   git clone https://github.com/OS-Copilot/FRIDAY.git
   ```

2. **Set Up Python Environment:** Ensure you have a version 3.10 or higher Python environment. You can create and
   activate this environment using the following commands, replacing `FRIDAY_env` with your preferred environment
   name:

   ```
   conda create -n FRIDAY_env python=3.10 -y
   conda activate FRIDAY_env
   ```

3. **Install Dependencies:** Move into the `FRIDAY` directory and install the necessary dependencies by running:

   ```
   cd FRIDAY
   pip install -r requirements.txt
   ```

4. **Set OpenAI API Key:** Configure your OpenAI API key in [.env](.env) and select the model you wish to use.

5. **Execute Your Task:** Run the following command to start FRIDAY. Replace `[query]` with your task as needed. By default, the task is *"Move the text files containing the word 'agent' from the folder named 'document' to the path 'working_dir/agent'"*.  If the task requires using related files, you can use `--query_file_path [file_path]`.
   ```
   python run.py --query [query]
   ```

\* FRIDAY currently only supports single-round conversation.

## 🛠️ FRIDAY-Gizmos
We maintain an open-source library of toolkits for FRIDAY, which includes tools that can be directly utilized within FRIDAY.
For a detailed list of tools, please see [FRIDAY-Gizmos](https://github.com/OS-Copilot/FRIDAY-Gizmos). The usage methods are as follows:

1. Find the tool you want to use in [FRIDAY-Gizmos](https://github.com/OS-Copilot/FRIDAY-Gizmos) and download its tool code.
2. Add the tool to FRIDAY's toolkit:
```shell
python friday/core/action_manager.py --add --tool_name [tool_name] --tool_path [tool_path]
```
3. If you wish to remove a tool, you can run:
```shell
python friday/core/action_manager.py --delete --tool_name [tool_name]
```

## 💻 User Interface (UI)

**Enhance Your Experience with Our Intuitive Frontend!** This interface is crafted for effortless control of your agents. For more details, visit [FRIDAY Frontend](https://github.com/OS-Copilot/FRIDAY-front).

## ✨ Deploy your own API tools with FastAPI
All FastAPIs are under： [friday/api](friday/api)
1. **Prepare your FastAPI file:** Create a new api folder under [friday/api](friday/api) and put your FastAPi python files under that folder.
2. **Import your FastAPI in API server:** Import your apis in [friday/core/api_server.py](friday/core/api_server.py)：
```python
import os

from fastapi import FastAPI
from friday.core.server_config import ConfigManager

app = FastAPI()


from friday.api.bing.bing_service import router as bing_router
#[TODO] Import your own api here


from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        print(f"Incoming request: {request.method} {request.url}")
        try:
            response = await call_next(request)
        except Exception as e:
            print(f"Request error: {str(e)}")
            raise e from None
        else:
            print(f"Outgoing response: {response.status_code}")
        return response


app.add_middleware(LoggingMiddleware)

# Create a dictionary that maps service names to their routers
services = {
    "bing": bing_router,
    # [TODO] Add your api router here

}

server_list = [
    "bing",
    # [TODO] Add your api's service name here.
]

# Include only the routers for the services listed in server_list
for service in server_list:
    if service in services:
        app.include_router(services[service])

# proxy_manager = ConfigManager()
# proxy_manager.apply_proxies()

if __name__ == "__main__":
    import uvicorn
    # you can change your port anyway
    uvicorn.run(app, host="0.0.0.0", port=8079)
```
3. **Run API server:**
Run the server in localhost,or deploy it on your web server:
```
python api_server.py
```
4. **Update API documentation:** 

Update the API documentation located in [friday/core/openapi.json](friday/core/openapi.json). After launching the API server, you can access the current OpenAPI documentation at `http://localhost:8079/openapi.json`.

Ensure to thoroughly update each API's summary in the documentation to clearly explain its functionality and usage. This is crucial as FRIDAY relies on these descriptions to understand the purpose of each API.

For example:
```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "FastAPI",
    "version": "0.1.0"
  },
  "paths": {  
    "/tools/audio2text": {
      "post": {
        // [TODO] change the summary to describe the usage of your api.
        "summary": "A tool that converts audio to natural language text",
        "operationId": "audio2text_tools_audio2text_post",
        "requestBody": {
          "content": {
            "multipart/form-data": {
              "schema": {
                "$ref": "#/components/schemas/Body_audio2text_tools_audio2text_post"
              }
            }
          },
          "required": true
        },
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {}
              }
            }
          },
          "422": {
            "description": "Validation Error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        }
      }
    },
    
  },
  "components": {
    "schemas": {
      "Body_audio2text_tools_audio2text_post": {
        "properties": {
          "file": {
            "type": "string",
            "format": "binary",
            "title": "File"
          }
        },
        "type": "object",
        "required": [
          "file"
        ],
        "title": "Body_audio2text_tools_audio2text_post"
      },
      
      
    }
  }
}
```

5. **Change the base url of tool_request_util.py:** FRIDAY utilizes the script located at [friday/core/tool_request_util.py](friday/core/tool_request_util.py) to interface with your API tools. After deploying your APIs, make sure to update the base URL in this file to match your API server's URL.
```python
import requests
class ToolRequestUtil:
    def __init__(self):
        self.session = requests.session()
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
        # [TODO] Change the base url
        self.base_url = "http://localhost:8079"

    def request(self, api_path, method, params=None, files=None, content_type="application/json"):
        """
        :param api_path: the path of the api
        :param method: get/post
        :param params: the params of the api, can be None
        :param files: files to be uploaded, can be None
        :param content_type: the content_type of api, e.g., application/json, multipart/form-data, can be None
        :return: the return of the api
        """
        url = self.base_url + api_path
        try:
            if method.lower() == "get":
                if content_type == "application/json":
                    result = self.session.get(url=url, json=params, headers=self.headers, timeout=60).json()
                else: 
                    result = self.session.get(url=url, params=params, headers=self.headers, timeout=60).json()
            elif method.lower() == "post":
                if content_type == "multipart/form-data":
                    result = self.session.post(url=url, files=files, data=params, headers=self.headers).json()
                elif content_type == "application/json":
                    result = self.session.post(url=url, json=params, headers=self.headers).json()
                else:
                    result = self.session.post(url=url, data=params, headers=self.headers).json()
            else:
                print("request method error!")
                return None
            return result
        except Exception as e:
            print("http request error: %s" % e)
            return None
```
<!-- ## 👨‍💻‍ Contributors

<a href="">
  <img src="" />
</a>

Made with [contrib.rocks](https://contrib.rocks). -->

## 🛡 Disclaimer

OS-Copilot is provided "as is" without warranty of any kind. Users assume full responsibility for any risks associated with its use, including **potential data loss** or **changes to system settings**. The developers of OS-Copilot are not liable for any damages or losses resulting from its use. Users must ensure their actions comply with applicable laws and regulations.


## 🏫 Community

Join our community to connect with other agent enthusiasts, share your tools and demos, and collaborate on exciting initiatives. You can find us on [Slack](https://join.slack.com/t/slack-ped8294/shared_invite/zt-2cqebow90-soac9UFKGZ2RcUy8PqjZrA).


## 🔎 Citation

```
@misc{wu2024oscopilot,
      title={OS-Copilot: Towards Generalist Computer Agents with Self-Improvement}, 
      author={Zhiyong Wu and Chengcheng Han and Zichen Ding and Zhenmin Weng and Zhoumianze Liu and Shunyu Yao and Tao Yu and Lingpeng Kong},
      year={2024},
      eprint={2402.07456},
      archivePrefix={arXiv},
      primaryClass={cs.AI}
}
```


## 📬 Contact

If you have any inquiries, suggestions, or wish to contact us for any reason, we warmly invite you to email us at wuzhiyong@pjlab.org.cn.