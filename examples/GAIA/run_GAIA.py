from oscopilot import FridayAgent
from oscopilot import FridayExecutor, FridayPlanner, FridayRetriever
from oscopilot.utils import setup_config, GAIALoader


args = setup_config()

agent = FridayAgent(FridayPlanner, FridayRetriever, FridayExecutor, config=args)

gaia = GAIALoader(args.level, args.dataset_cache)

if args.gaia_task_id:
    task = gaia.get_data_by_task_id(args.gaia_task_id, args.dataset_type)
    query = gaia.task2query(task)
    agent.run(query)
else:
    task_lst = gaia.dataset[args.dataset_type]
    for task in task_lst:
        query = gaia.task2query(task)
        agent.run(query)