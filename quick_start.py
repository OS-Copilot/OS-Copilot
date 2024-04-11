from oscopilot import FridayAgent
from oscopilot import ToolManager
from oscopilot import FridayExecutor, FridayPlanner, FridayRetriever
from oscopilot.utils import setup_config, setup_pre_run

args = setup_config()
if not args.query:
    # args.query = "Create a new folder named 'test_friday'"
    args.query = "用python将工作目录下的document文件夹中包含'agent'这个单词的文件复制到工作目录下的agent文件夹中"
task = setup_pre_run(args)
agent = FridayAgent(FridayPlanner, FridayRetriever, FridayExecutor, ToolManager, config=args)
agent.run(task=task)