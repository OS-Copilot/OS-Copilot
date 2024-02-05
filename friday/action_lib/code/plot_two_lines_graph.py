from jarvis.action.base_action import BaseAction
import matplotlib.pyplot as plt
import pandas as pd
import os

class plot_two_lines_graph(BaseAction):
    def __init__(self):
        self._description = "Use matplotlib to plot the data into a line graph with 'x' as the horizontal axis and 'y1' and 'y2' as the vertical axes, then save the graph as 'lines.png' in the working directory."

    def __call__(self, data, output_filename='lines.png', working_directory=None, *args, **kwargs):
        """
        Plots the data into a line graph using matplotlib and saves the graph as an image in the working directory.

        Args:
            data (dict): A dictionary containing the data to be plotted with 'x' as keys and 'y1', 'y2' as values.
            output_filename (str, optional): The filename for the saved plot image. Defaults to 'lines.png'.
            working_directory (str, optional): The working directory where the file operations should be performed. If not provided, the current working directory will be used.

        Returns:
            None
        """
        # Change the current working directory to the provided working_directory if provided
        if working_directory:
            os.chdir(working_directory)

        # Extract x and y values from the data
        x_values = data['x']
        y1_values = data['y1']
        y2_values = data['y2']

        # Create a figure and axis for the plot
        fig, ax = plt.subplots()

        # Plot the data
        ax.plot(x_values, y1_values, label='y1')
        ax.plot(x_values, y2_values, label='y2')

        # Set the labels and title
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title('Line Graph')

        # Add a legend
        ax.legend()

        # Save the plot to the output_filename
        plt.savefig(output_filename)

        # Print completion message
        print(f"Plotting completed. Graph saved as {output_filename}.")

# Example of how to use the class (this should be in the comments):
plotter = plot_two_lines_graph()
data = {'x': [1, 2, 3, 4, 5], 'y1': [1, 2, 3, 4, 5], 'y2': [2, 4, 6, 8, 10]}
plotter(data, "lines.png", "/home/heroding/桌面/Jarvis/working_dir")