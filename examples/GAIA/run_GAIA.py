import json
import requests
from oscopilot import FridayAgent
from oscopilot import FridayExecutor, FridayPlanner, FridayRetriever, ToolManager
from oscopilot.utils import setup_config, GAIALoader, GAIA_postprocess


args = setup_config()
args.dataset_type = 'validation'
model = 'gpt4-turbo'

write_file_path = 'gaia_{}_{}_level{}_results.jsonl'.format(model, args.dataset_type, args.level)
def get_numbers(path):
    correct = 0
    incomplete = 0
    with open(path, 'r', encoding='utf-8') as file:
        data = [json.loads(line) for line in file]
        print(data)
        for d in data:
            if d["model_answer"] == d["groundtruth"]:
                correct += 1
            if d["model_answer"] == "" or d["model_answer"] == "incomplete":
                incomplete += 1
        if len(data) > 0:
            return correct, incomplete, data[-1]["index"]
        return correct, incomplete, -1 # -1 denotes no previous running

agent = FridayAgent(FridayPlanner, FridayRetriever, FridayExecutor, ToolManager, config=args)

gaia = GAIALoader(args.level, args.dataset_cache)

# args.gaia_task_id = "e1fc63a2-da7a-432f-be78-7c4a95598703"
if args.gaia_task_id:
    task = gaia.get_data_by_task_id(args.gaia_task_id, args.dataset_type)
    query = gaia.task2query(task)
    # agent.run(query)
    # if agent.inner_monologue.result != '':
    if True:
        # print(agent.inner_monologue.result)
        result = """17000
        """
        # result = GAIA_postprocess(task['Question'], agent.inner_monologue.result)
        result = GAIA_postprocess(task['Question'], result)
        print('The answer of GAIA Task {0} : {1}'.format(args.gaia_task_id, result))
else:
    task_lst = gaia.dataset[args.dataset_type]
    correct, incomplete, last_run_index = get_numbers(write_file_path)
    print(correct, incomplete, last_run_index)
    with open(write_file_path, 'a', encoding='utf-8') as file:
        count = 0

        for task in task_lst:
            if count <= last_run_index:
                print("\t\t\t skip current run:", count)
                count += 1
                continue
            query = gaia.task2query(task)
            result = ''
            # agent.run(query)
            try:
                agent.run(query)
                print("$$$$$$" * 30)
                if agent.inner_monologue.result != '':
                    result = GAIA_postprocess(task['Question'], agent.inner_monologue.result)
            except requests.exceptions.ConnectionError as ConnectionError:
                print(f"Connection error.: {ConnectionError}")
                exit()
            except Exception as e:
                print("$$$$$$" * 30)
                # Code to handle any other type of exception
                print(f"An error occurred: {e}")
                print("$$$$$$" * 30)
                result = "incomplete"
                incomplete += 1
            output_dict = {
                "index": count,
                "task_id": task['task_id'],
                "model_answer": result,
                "groundtruth": task["Final answer"],
                "reasoning_trace": ""
            }
            if result == task["Final answer"]:
                correct += 1
            json_str = json.dumps(output_dict)
            file.write(json_str + '\n')
            file.flush()
            count += 1
            # if count > 2:
            #     break
        print("accuracy:", correct / count)
        print("incomplete:", incomplete / count)
        print("correct incomplete total,", correct, incomplete, count)
