from setuptools import setup, find_packages


with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="os-copilot",
    version="0.1.0",
    author="Zhiyong Wu and Chengcheng Han and Zichen Ding and Zhenmin Weng and Zhoumianze Liu and Shunyu Yao and Tao Yu and Lingpeng Kong",
    author_email="wuzhiyong@pjlab.org.cn, hccngu@163.com",
    description="An self-improving embodied conversational agents seamlessly integrated into the operating system to automate our daily tasks.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/OS-Copilot/OS-Copilot",
    license="MIT",

    packages=find_packages(exclude=("docs", "temp", "pic", "log")),

    install_requires=requirements,

    entry_points={
        "console_scripts": [
            "friday=quick_start:main",
        ],
    },

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="AI, LLMs, Large Language Models, Agent, OS, Operating System",

    python_requires='>=3.10',
)
