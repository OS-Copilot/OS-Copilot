# OS-Copilot: Towards Generalist Computer Agents with Self-Improvement

<div align="center">

[[Website]](https://os-copilot.github.io/)
[[PDF]](https://arxiv.org/pdf/2402.07456.pdf)
[[Documentation]](https://os-copilot.readthedocs.io/en/latest/)
[[Twitter]](https://twitter.com/oscopilot)
[[Discord]](https://discord.gg/PDsRrEV27b)
<!-- [[Arxiv]](https://arxiv.org/abs/2402.07456) -->
<!-- [[Tweet]](https://twitter.com/DrJimFan/status/1662115266933972993?s=20) -->

[![Static Badge](https://img.shields.io/badge/MIT-License-green)](https://github.com/OS-Copilot/OS-Copilot/blob/main/LICENSE)
![Static Badge](https://img.shields.io/badge/python-3.10-blue)
[![Static Badge](https://img.shields.io/badge/FRIDAY-Frontend-yellow)](https://github.com/OS-Copilot/FRIDAY-front)



<p align="center">
  <img src='pic/demo.png' width="100%">
</p>

</div>

<!-- ## 📖 Overview

- **OS-Copilot** is a pioneering conceptual framework for building generalist computer agents on Linux and MacOS, which provides a unified interface for app interactions in the heterogeneous OS ecosystem.
  
<p align="center">
  <img src='pic/framework.png' width="75%">
</p>

- Leveraging OS-Copilot, we built **FRIDAY**, a self-improving AI assistant capable of solving general computer tasks.

<p align="center">
  <img src='pic/FRIDAY.png' width="75%">
</p> -->

## ⚡️ Quickstart

1. **Clone the GitHub Repository:** 

   ```
   git clone https://github.com/OS-Copilot/OS-Copilot.git
   ```

2. **Set Up Python Environment:** Ensure you have a version 3.10 or higher Python environment. You can create and
   activate this environment using the following commands, replacing `oscopilot_env` with your preferred environment
   name:

   ```
   conda create -n oscopilot_env python=3.10 -y
   conda activate oscopilot_env
   ```

3. **Install Dependencies:** Move into the `OS-Copilot` directory and install the necessary dependencies by running:

   ```
   cd OS-Copilot
   pip install -e .
   ```

4. **Set OpenAI API Key:** Configure your OpenAI API key in [.env](.env) and select the model you wish to use.

5. **Running the Script:** Run the quick_start.py script, simply execute the following command in your terminal:
   ```
   python quick_start.py
   ```

\* FRIDAY currently only supports single-round conversation.

## 🛠️ Tutorial

| **Level**        | **Tutorial**                                                                                    | **Description**                                                                                                                      |
|------------------|-------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------|
| **Beginner**     | [Installation](https://os-copilot.readthedocs.io/en/latest/installation.html)| Provides three methods to install FRIDAY: cloning from GitHub, development setup via pip install -e ., and direct pip installation.  |
| **Beginner**     | [Getting Started](https://os-copilot.readthedocs.io/en/latest/quick_start.html)| Demonstrates how to use FRIDAY with a quick_start.py script, covering module imports, configuration setup, and task execution.       |
| **Intermediate** | [Adding Your Tools](https://os-copilot.readthedocs.io/en/latest/tutorials/add_tool.html)| Outlines the process for adding and removing tools to the FRIDAY.                                                                    |
| **Intermediate** | [Deploying API Services](https://os-copilot.readthedocs.io/en/latest/tutorials/deploy_api_service.html)| Explains the deployment of API services for FRIDAY, including environment setup, configuring API tools, and launching the server.    |
| **Intermediate** | [Example: Automating Excel Tasks](https://os-copilot.readthedocs.io/en/latest/tutorials/example_excel.html)| Demonstrates automating Excel tasks with FRIDAY, including formula application and chart creation within an Excel sheet.             |
| **Intermediate** | [Enhancing FRIDAY with Self-Learning for Excel Task Automation](https://os-copilot.readthedocs.io/en/latest/tutorials/self_learning.html) | Showcases empowering FRIDAY with self-learning to autonomously learn and execute Excel file manipulations.                           |
| **Advanced**     | [Designing New API Tools](https://os-copilot.readthedocs.io/en/latest/tutorials/design_new_api_tool.html)| Guides on designing, integrating, and deploying custom API tools for FRIDAY to extend its functionalities.                           |


<!-- ## 🛠️ FRIDAY-Gizmos
We maintain an open-source library of toolkits for FRIDAY, which includes tools that can be directly utilized within FRIDAY.
For a detailed list of tools, please see [FRIDAY-Gizmos](https://github.com/OS-Copilot/FRIDAY-Gizmos). The usage methods are as follows:

1. Find the tool you want to use in [FRIDAY-Gizmos](https://github.com/OS-Copilot/FRIDAY-Gizmos) and download its tool code.
2. Add the tool to FRIDAY's toolkit:
```shell
python friday/tool_repository/manager/tool_manager.py --add --tool_name [tool_name] --tool_path [tool_path]
```
3. If you wish to remove a tool, you can run:
```shell
python friday/tool_repository/manager/tool_manager.py --delete --tool_name [tool_name]
```

## 💻 User Interface (UI)

**Enhance Your Experience with Our Intuitive Frontend!** This interface is crafted for effortless control of your agents. For more details, visit [FRIDAY Frontend](https://github.com/OS-Copilot/FRIDAY-front).

## ✨ Deploy API Services

For comprehensive guidelines on deploying API services, please refer to the [OS-Copilot documentation](https://os-copilot.readthedocs.io/en/latest/).  -->

## 🏫 Community

Join our community to connect with other enthusiasts, share your tools and demos, and collaborate on innovative projects. Stay engaged and get the latest updates by following us:

- **Discord**: Join our Discord server for real-time discussions, support, and to share your work with the community. Click here to join: [Discord Server](https://discord.gg/PDsRrEV27b).
- **Twitter**: Follow us on Twitter [@oscopilot](https://twitter.com/oscopilot) for the latest news, updates, and highlights from our community.

## 👨‍💻‍ Contributors

<a href="https://github.com/OS-Copilot/OS-Copilot/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=OS-Copilot/OS-Copilot" />
</a>

<!-- Made with [contrib.rocks](https://contrib.rocks). -->

## 🛡 Disclaimer

OS-Copilot is provided "as is" without warranty of any kind. Users assume full responsibility for any risks associated with its use, including **potential data loss** or **changes to system settings**. The developers of OS-Copilot are not liable for any damages or losses resulting from its use. Users must ensure their actions comply with applicable laws and regulations.


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