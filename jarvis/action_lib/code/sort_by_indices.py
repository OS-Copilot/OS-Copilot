from jarvis.action.base_action import BaseAction

class sort_by_indices(BaseAction):
    def __init__(self):
        self._description = "Sorts an array based on the order defined in a separate list of indices."

    def __call__(self, arr, indices, *args, **kwargs):
        """
        Sorts an array based on the order defined in a separate list of indices.

        Args:
        arr (list): The list of strings to be sorted.
        indices (list): A list of integers representing the desired order of elements in 'arr'.
                    Each integer in 'indices' is an index in 'arr' that specifies the order.
        
        Returns:
        list: A new list of strings from 'arr' arranged according to the order specified in 'indices'.
        """
        # Create the new number based on the specified order
        new_number = ''.join(arr[i - 1] for i in indices)
        
        # Print the task execution completion message
        print(f"New 9-digit number created: {new_number}")
        
        return new_number

sort = sort_by_indices()
ordered_list = sort(["2", "0", "3", "0", "7", "3", "9", "0", "2"], [5, 8, 7, 3, 6, 4, 9, 2, 1])