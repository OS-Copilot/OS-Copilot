from jarvis.action.base_action import BaseAction
import pandas as pd
import os

class extract_excel_content(BaseAction):
    def __init__(self):
        self._description = "Extract the full text content of the specified Excel file."

    def __call__(self, excel_file_path, *args, **kwargs):
        """
        Extract the full text content of the specified Excel file and return its content.

        Args:
            excel_file_path (str): The absolute path to the Excel file to be read.

        Returns:
            dict: A dictionary where each key is the sheet name and each value is the content of that sheet as a DataFrame.
        """
        try:
            # Read the Excel file
            with pd.ExcelFile(excel_file_path) as xls:
                # Dictionary to store content of each sheet
                sheets_content = {}
                max_rows = 0
                max_columns = 0
                for sheet_name in xls.sheet_names:
                    # Read each sheet into a DataFrame
                    df = pd.read_excel(xls, sheet_name)
                    sheets_content[sheet_name] = df
                    max_rows = max(max_rows, df.shape[0])
                    max_columns = max(max_columns, df.shape[1])
            pd.set_option('display.max_rows', max_rows)
            pd.set_option('display.max_columns', max_columns)
            print(f"Task execution complete. Content of the Excel file {excel_file_path} extracted successfully.")
            return sheets_content
        except FileNotFoundError:
            print(f"The Excel file {excel_file_path} does not exist.")
        except Exception as e:
            print(f"An error occurred while reading the Excel file {excel_file_path}: {e}")

# Example of how to use the class (this should be in the comments):
# extractor = extract_excel_content()
# content = extractor(excel_file_path='/home/heroding/.cache/huggingface/datasets/downloads/9fbb70f8ea7240bdd24693c968fa879fd2e186fdedf2d1e709c59e096c865b25.xlsx')
