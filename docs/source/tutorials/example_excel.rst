Example: Automating Excel Tasks with FRIDAY
================================================

In this tutorial, we'll showcase how FRIDAY can be utilized for manipulating Excel files, automating tasks that would otherwise be tedious and time-consuming. We'll take on a specific task involving Excel file operations as an example.

Task Overview
-------------

You are required to perform several tasks related to Excel manipulation involving an experiment's data recorded in a sheet named "Sheet1". The tasks include:

- Applying a formula across rows in column B.
- Creating a scatter chart within "Sheet1" that plots acceleration (y-axis) against the hanging mass (x-axis).
- Labeling the chart axes with the appropriate column headers.

The Excel file for this task is located in `working_dir` and is named "Dragging.xlsx".

Step-by-Step Guide
------------------

1. **Preparing the Necessary Tools**:

   Locate the following tools within `FRIDAY-Gizmos/Excel` directory:

   - ``apply_formula_to_column_B``
   - ``create_new_sheet_for_chart``
   - ``insert_scatter_chart``
   - ``read_excel_sheet``

   Follow the steps outlined in the "Adding Your First Tool" tutorial to add these four tools to FRIDAY's tool repository.

2. **Executing the Task**:

   To perform the Excel manipulation task, run the following command in your terminal. This command instructs FRIDAY to apply the necessary operations on the "Dragging.xlsx" file based on the provided task description.

   .. code-block:: shell

      python quick_start.py --query "You need to do some tasks related to excel manipulation.\n My sheet records data from an experiment where one hanging block (m2) drags a block (m1=0.75 kg) on a frictionless table via a rope around a frictionless and massless pulley. It has a sheet called Sheet1. \n Your task is: Fill out the rest rows in column B using the formula in B2. Create a scatter chart in Sheet1 with acceleration on the y-axis and the hanging mass on the x-axis. Add the corresponding column headers as the axis labels. \n You should complete the task and save the result directly in this excel file." --query_file_path "working_dir/Dragging.xlsx"

Conclusion
----------

Upon completion, the "Dragging.xlsx" file will have the specified formula applied across rows in column B, and a scatter chart will be created in "Sheet1" as requested. This example illustrates how FRIDAY can automate complex Excel operations, saving time and reducing the potential for manual errors.

Ensure to adjust file paths and names as per your specific setup. This tutorial demonstrates the power and flexibility of FRIDAY in handling and automating tasks within Excel, showcasing its capability to significantly streamline such processes.
