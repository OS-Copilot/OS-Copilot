import json
from oscopilot import FridayAgent
from oscopilot import FridayExecutor, FridayPlanner, FridayRetriever, ToolManager
from oscopilot.utils import setup_config, GAIALoader, GAIA_postprocess


args = setup_config()

agent = FridayAgent(FridayPlanner, FridayRetriever, FridayExecutor, ToolManager, config=args)

gaia = GAIALoader(args.level, args.dataset_cache)

args.gaia_task_id = "07ed8ebc-535a-4c2f-9677-3e434a08f7fd"
if args.gaia_task_id:
    task = gaia.get_data_by_task_id(args.gaia_task_id, args.dataset_type)
    query = gaia.task2query(task)
    agent.run(query)
    if agent.inner_monologue.result != '':
        result = GAIA_postprocess(task['Question'], agent.inner_monologue.result)
        print('The answer of GAIA Task {0} : {1}'.format(args.gaia_task_id, result))
else:
    task_lst = gaia.dataset[args.dataset_type]
    with open('gaia_{}_level{}_results.jsonl'.format(args.dataset_type, args.level), 'w', encoding='utf-8') as file:
        count = 0
        for task in task_lst:
            query = gaia.task2query(task)
            agent.run(query)
            if agent.inner_monologue.result != '':
                result = GAIA_postprocess(task['Question'], agent.inner_monologue.result)
            else:
                result = ''
            output_dict = {
                "task_id": task['task_id'], 
                "model_answer": result, 
                "reasoning_trace": ""
            }
            json_str = json.dumps(output_dict)
            file.write(json_str + '\n')
            file.flush()
            count += 1
            if count > 10:
                break
