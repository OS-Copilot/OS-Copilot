from oscopilot import FridayAgent
from oscopilot import FridayExecutor, FridayPlanner, FridayRetriever, ToolManager
from oscopilot.utils import setup_config, SheetTaskLoader


args = setup_config()
sheet_task_loader = SheetTaskLoader("examples/SheetCopilot/sheet_task.jsonl")
agent = FridayAgent(FridayPlanner, FridayRetriever, FridayExecutor, ToolManager, config=args)

if args.sheet_task_id:
    task = sheet_task_loader.get_data_by_task_id(args.sheet_task_id)
    agent.run(task)
else:
    task_lst = sheet_task_loader.load_sheet_task_dataset()
    for task_id, task in enumerate(task_lst):
        args.sheet_task_id = task_id
        agent.run(task)