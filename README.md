# OS-Copilot: Towards Generalist Computer Agents with Self-Improvement

<div align="center">

[[Website]](https://os-copilot.github.io/)
[[Arxiv]]()
[[PDF]]()
<!-- [[Tweet]](https://twitter.com/DrJimFan/status/1662115266933972993?s=20) -->

[![Static Badge](https://img.shields.io/badge/MIT-License-green)](https://github.com/OS-Copilot/FRIDAY/blob/main/LICENSE)
![Static Badge](https://img.shields.io/badge/python-3.10-blue)

<p align="center">
  <img src='pic/demo.png' width=550>
</p>

</div>

## 📖 Overview

- **OS-Copilot** is a pioneering conceptual framework for building generalist computer agents on Linux and MacOS, which provides a unified interface for app interactions in the heterogeneous OS ecosystem.
  
<p align="center">
  <img src='pic/framework.png' width=550>
</p>

- Leveraging OS-Copilot, we built **FRIDAY**, a self-improving AI assistant capable of solving general computer tasks.

<p align="center">
  <img src='pic/FRIDAY.png' width=550>
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

4. **Set OpenAI API Key:** Configure your OpenAI API key in `config.json` and select the model you wish to use.

5. **Execute Your Task:** Run the following command to start FRIDAY. Replace `[query]` with your task as needed. By default, the task is *"Move the text files containing the word 'agent' from the folder named 'document' to the path 'working_dir/agent'"*.  If the task requires using related files, you can use `--query_file_path [file_path]`.
   ```
   python run.py --query [query]
   ```


<!-- ## 👨‍💻‍ Contributors

<a href="">
  <img src="" />
</a>

Made with [contrib.rocks](https://contrib.rocks). -->


## 🔎 Citation

```
@misc{
}
```


## 📬 Contact

If you have any inquiries, suggestions, or wish to contact us for any reason, we warmly invite you to email us at .