import os
import argparse
import logging
from datasets import load_dataset
from jarvis.agent.jarvis_agent import JarvisAgent
from data_id import data_id

class GAIALoader:
    def __init__(self, cache_dir=None):
        if cache_dir != None:
            assert os.path.exists(cache_dir), f"Cache directory {cache_dir} does not exist."
            self.cache_dir = cache_dir
            try:
                self.dataset = load_dataset("gaia-benchmark/GAIA", "2023_level1", cache_dir=self.cache_dir)
            except Exception as e:
                raise Exception(f"Failed to load GAIA dataset: {e}")
        else:
            self.dataset = load_dataset("gaia-benchmark/GAIA", "2023_level1")
            
        
    def get_data_by_task_id(self, task_id, type):
        if self.dataset is None or type not in self.dataset:
            raise ValueError("Dataset not loaded or data set not available.")

        data_set = self.dataset[type]
        for record in data_set:
            if record['task_id'] == task_id:
                return record
        return None
    

def main():
    parser = argparse.ArgumentParser(description='Inputs')
    parser.add_argument('--action_lib_path', type=str, default='../jarvis/action_lib', help='tool repo path')
    parser.add_argument('--config_path', type=str, default='config.json', help='openAI config file path')
    parser.add_argument('--task_id', type=str, default=None, help='GAIA dataset task_id')
    parser.add_argument('--cache_dir', type=str, default=None, help='GAIA dataset cache dir path')
    parser.add_argument('--logging_filedir', type=str, default='log/test_level1', help='GAIA dataset cache dir path')
    parser.add_argument('--data_type', type=str, default='test', help='GAIA dataset data type')
    parser.add_argument('--level', type=str, default='level1', help='GAIA dataset data level')
    args = parser.parse_args()

    # init jarvis
    jarvis_agent = JarvisAgent(config_path=args.config_path, action_lib_dir=args.action_lib_path)
    # get task list
    task_list = data_id[args.data_type][args.level]
    
    # execute task list
    for task_id in task_list:   
        logging.basicConfig(filename=os.path.join(args.logging_filedir, "{}.log".format(task_id)), level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

        print('Use the task_id {} to get the corresponding question in the GAIA dataset.'.format(task_id))
        data = GAIALoader(args.cache_dir).get_data_by_task_id(task_id, "test")
        task = 'Your task is: {0}'.format(data['Question'])
        if data['file_name'] != '':
            task = task + '\nThe path of the files you need to use: {0}.{1}'.format(data['file_path'], data['file_name'].split('.')[-1])

        print('Task:\n'+task)
        logging.info(task)

        # run 
        jarvis_agent.run(task)
        
if __name__ == '__main__':
    main()

