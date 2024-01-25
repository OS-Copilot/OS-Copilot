from jarvis.action.base_action import BaseAction
import matplotlib.pyplot as plt
import pandas as pd
import os

class plot_line_graph(BaseAction):
    def __init__(self):
        self._description = "Use matplotlib to plot the data into a line graph."

    def __call__(self, data, output_path=None, working_directory=None, *args, **kwargs):
        """
        Plots the data into a line graph using matplotlib and optionally saves the plot as an image.

        Args:
            data (dict): A dictionary containing the data to be plotted. The keys are the x-axis labels and the values are the y-axis values.
            output_path (str, optional): The path where the plot image will be saved. If not provided, the plot will not be saved.
            working_directory (str, optional): The working directory where the file operations should be performed. If not provided, the current working directory will be used.

        Returns:
            None
        """
        # Change the current working directory to the provided working_directory if provided
        if working_directory:
            os.chdir(working_directory)

        # Extract x and y values from the data
        x_values = list(data.keys())
        y_values = list(data.values())

        # Create a figure and axis for the plot
        fig, ax = plt.subplots()

        # Plot the data
        ax.plot(x_values, y_values)

        # Set the labels and title
        ax.set_xlabel('X-axis')
        ax.set_ylabel('Y-axis')
        ax.set_title('Line Graph')

        # Optionally save the plot to the output_path
        if output_path:
            plt.savefig(output_path)

        # Show the plot
        plt.show()

        # Print completion message
        print("Plotting completed.")

# Example of how to use the class (this should be in the comments):
# plotter = plot_line_graph()
# data = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5}
# plotter(data, "/home/heroding/桌面/Jarvis/working_dir/line.png", "/home/heroding/桌面/Jarvis/working_dir")