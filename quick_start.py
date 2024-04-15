from oscopilot import FridayAgent
from oscopilot import ToolManager
from oscopilot import FridayExecutor, FridayPlanner, FridayRetriever
from oscopilot.utils import setup_config, setup_pre_run

args = setup_config()
if not args.query:
    # args.query = "Create a new folder named 'test_friday'"
    # args.query = "用python将工作目录下的document文件夹中包含'agent'这个单词的文件复制到工作目录下的agent文件夹中"
    # args.query = "You need to do some tasks related to excel manipulation.\n My sheet records data from an experiment where one hanging block (m2) drags a block (m1=0.75 kg) on a frictionless table via a rope around a frictionless and massless pulley. It has a sheet called Sheet1. \n Your task is: Fill out the rest rows in column B using the formula in B2. Create a scatter chart in Sheet1 with acceleration on the y-axis and the hanging mass on the x-axis. Add the corresponding column headers as the axis labels. \n You should complete the task and save the result directly in this excel file. 可以使用openpyxl包。"
    # args.query_file_path = "working_dir/Dragging.xlsx"
    args.query = "使用plotly随便写几个功能，不要检查plotly是否安装"
task = setup_pre_run(args)
agent = FridayAgent(FridayPlanner, FridayRetriever, FridayExecutor, ToolManager, config=args)
agent.run(task=task)