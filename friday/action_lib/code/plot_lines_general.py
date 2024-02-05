from jarvis.action.base_action import BaseAction
import matplotlib.pyplot as plt

class plot_lines_general(BaseAction):
    def __init__(self):
        self._description = "Plots lines connecting numbers and letters based on the given connections and optionally saves the plot as an image."

    def __call__(self, connections, numbers, letters, path):
        """
        Plots lines connecting numbers and letters based on the given connections and optionally saves the plot as an image.

        Parameters:
        connections (dict): A dictionary where keys are numbers and values are letters, representing the connections. The format of the dictionary key is a number, and the format of the value is a string.
        numbers (list): A list of numbers to be plotted.
        letters (list): A list of letters to be plotted. The order of letters should correspond to the order of numbers.
        path (string): Save the plot as an image with the path.

        Output:
        A matplotlib plot showing the connections between the numbers and letters.
        """

        # Determine positions for letters
        # letter_positions = {letter: i + 1 for i, letter in enumerate(letters)}

        # plt.figure(figsize=(10, 6))

        # # Plotting the numbers and letters on the x-axis
        # plt.plot(numbers, [1] * len(numbers), 'o', color='blue')  # Numbers
        # plt.plot(numbers, [0] * len(letters), 'o', color='red')  # Letters

        # # Drawing lines between the numbers and letters
        # for num, letter in connections.items():
        #     if letter in letter_positions:
        #         plt.plot([num, letter_positions[letter]], [1, 0], color='green')

        # plt.title("Line Connections")
        # plt.yticks([0, 1], ['Letters', 'Numbers'])
        # plt.xticks(range(1, len(numbers) + 1))
        # plt.grid(True)
        # if path:
        #     plt.savefig(path)
        # plt.show()

        # Determine positions for letters
        letter_positions = {letter: i + 1 for i, letter in enumerate(letters)}

        # Create a figure for plotting
        plt.figure(figsize=(10, 6))

        # Plotting the numbers and letters on the x-axis
        plt.plot(numbers, [1] * len(numbers), 'o', color='blue')  # Numbers
        plt.plot(numbers, [0] * len(letters), 'o', color='red')  # Letters

        # Drawing lines between the numbers and letters
        for num, letter in connections.items():
            if letter in letter_positions:
                plt.plot([num, letter_positions[letter]], [1, 0], color='green')

        # Set the title and labels for the plot
        plt.title("Line Connections")
        plt.yticks([0, 1], ['Letters', 'Numbers'])
        plt.xticks(range(1, len(numbers) + 1))
        plt.grid(True)

        # Save the plot as an image
        plt.savefig(path)
        plt.close()

# Example of how to use the class
plot_lines = plot_lines_general()
plot = plot_lines({1:"e",5:"a",2:"b",4:"d"}, [1, 2, 3, 4, 5], ['a', 'b', 'c', 'd', 'e'], "/home/heroding/桌面/Jarvis/working_dir/plot.png")


