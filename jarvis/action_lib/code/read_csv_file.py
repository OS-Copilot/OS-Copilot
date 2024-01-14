from jarvis.action.base_action import BaseAction
import pandas as pd
import os

class read_csv_file(BaseAction):
    def __init__(self):
        self._description = "Read the content of a CSV file to extract data."

    def __call__(self, csv_file_path, *args, **kwargs):
        """
        Read the content of the specified CSV file and return its content as a DataFrame.

        Args:
            csv_file_path (str): The absolute path to the CSV file to be read.

        Returns:
            DataFrame: The content of the CSV file as a pandas DataFrame.
        """
        try:
            # Change the current working directory to the directory of the CSV file
            dir_path = os.path.dirname(csv_file_path)
            os.chdir(dir_path)
            
            # Set the display options of Pandas to show all rows and columns
            pd.set_option('display.max_rows', None)
            pd.set_option('display.max_columns', None)

            # Read the CSV file
            data = pd.read_csv(os.path.basename(csv_file_path))
            print(f"Task execution complete. Content of the CSV file {csv_file_path} read successfully.")
            return data
        except FileNotFoundError:
            print(f"The CSV file {csv_file_path} does not exist.")
        except Exception as e:
            print(f"An error occurred while reading the CSV file {csv_file_path}: {e}")


# Example of how to use the class (this should be in the comments):
# reader = read_csv_file()
# penguin_data = reader(csv_file_path='/home/heroding/.cache/huggingface/datasets/downloads/f78694ef938cb07a34ab1ca2ccf515e1433c479ca40632f122d332288dda688b.csv')