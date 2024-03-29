Installation
========================

There are three ways to install OS-Copilot: using `pip` directly, cloning the GitHub repository, or through the `pip install -e .` method for a development setup. Please follow the instructions below based on your preferred installation method.

1. **Clone the GitHub Repository** (if not already done):

   .. code-block:: shell

      git clone https://github.com/OS-Copilot/OS-Copilot.git

2. **Navigate to the Repository Directory:**

   .. code-block:: shell

      cd OS-Copilot

3. **Set Up Python Environment:** Ensure you have a version 3.10 or higher Python environment. You can create and activate this environment using the following commands, replacing OS-Copilot_env with your preferred environment name:

   .. code-block:: shell

      conda create -n OS-Copilot_env python=3.10 -y
      conda activate OS-Copilot_env

3. **Install Dependencies:**  Install the necessary dependencies.

   - Option 1(Recommended): Use pip to install the project in editable mode.

   .. code-block:: shell

      pip install -e .

   - Option 2: You can install OS-Copilot directly using pip with the following command:

   .. code-block:: shell

      pip install os-copilot-agent
   
   - Option 3: Install the necessary dependencies:
   
   .. code-block:: shell

      cd OS-Copilot
      pip install -r requirements.txt

4. **Set OpenAI API Key:** Configure your OpenAI API key in the `.env` file and select the model you wish to use.

   .. code-block:: shell

      MODEL_NAME=""
      OPENAI_API_KEY=""