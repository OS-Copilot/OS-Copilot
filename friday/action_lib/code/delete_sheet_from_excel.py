from jarvis.action.base_action import BaseAction
import os
from collections import Counter
import openpyxl
from openpyxl.utils.exceptions import InvalidFileException

class delete_sheet_from_excel(BaseAction):
    def __init__(self):
        self._description = "Deletes a sheet with the specified name from an Excel workbook."

    def __call__(self, file_path: str, sheet_name: str) -> None:
        """
        Deletes a sheet with the specified name from an Excel workbook.

        Args:
        file_path (str): Path to the Excel file.
        sheet_name (str): Name of the sheet to be deleted.

        Returns:
         None
        """
        try:
            # Load the workbook
            workbook = openpyxl.load_workbook(file_path)

            # Check if the sheet name exists
            if sheet_name not in workbook.sheetnames:
                raise ValueError(f"No sheet named '{sheet_name}' found in the workbook.")

            # Remove the sheet
            sheet = workbook[sheet_name]
            workbook.remove(sheet)

            # Save the workbook
            workbook.save(file_path)

        except FileNotFoundError:
            raise FileNotFoundError(f"The file '{file_path}' was not found.")
        except InvalidFileException:
            raise InvalidFileException(f"The file '{file_path}' is not a valid Excel file.")

# Example usage:
# print(delete_sheet_from_excel()("/home/heroding/桌面/Jarvis/tasks/SheetTasks/sheets/BoomerangSales.xlsx", "Frequencies"))