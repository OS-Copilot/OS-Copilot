import json
import pandas as pd
from datasets import load_dataset, config

# 设置下载和缓存路径
config.HF_DATASETS_CACHE = "/Users/hanchengcheng/Documents/official_space/github/jarvis/tasks/GAIA"


def download_dataset():
    dataset = load_dataset('gaia-benchmark/GAIA', '2023_all')
    return dataset


def save_dataset_as_json(json_path):
    """
    Save a dataset from Hugging Face as a JSON file.

    Args:
    dataset_name (str): The name of the dataset to download.
    json_path (str): The file path where the JSON should be saved.
    """
    # 加载数据集
    dataset = download_dataset()

    # 以字典的形式提取数据
    dataset_dict = {split: dataset[split].to_dict() for split in dataset.keys()}

    # 保存为JSON文件
    with open(json_path, 'w', encoding='utf-8') as json_file:
        json.dump(dataset_dict, json_file, ensure_ascii=False, indent=4)


def save_dataset_as_csv(csv_path_prefix):
    """
    Save a dataset from Hugging Face as CSV files.

    Args:
    dataset_name (str): The name of the dataset to download.
    csv_path_prefix (str): The file path prefix where the CSVs should be saved.
    """
    # 加载数据集
    dataset = download_dataset()

    # 对于数据集中的每个拆分（如 train, test），将其保存为CSV
    for split in dataset.keys():
        # 转换为Pandas DataFrame
        df = pd.DataFrame(dataset[split])

        # 保存为CSV文件
        df.to_csv(f'{csv_path_prefix}_{split}.csv', index=False)

# 使用函数保存数据集为CSV
save_dataset_as_csv('/Users/hanchengcheng/Documents/official_space/github/jarvis/tasks/GAIA/all_dataset.csv')



# 使用函数保存数据集为JSON
# save_dataset_as_json('/Users/hanchengcheng/Documents/official_space/github/jarvis/tasks/GAIA/all_dataset.json')

# Example usage
# dataset = download_dataset()
# print(dataset)
