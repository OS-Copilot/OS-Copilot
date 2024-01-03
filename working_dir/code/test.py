from jarvis.action.base_action import BaseAction
import math

class calculate_towers(BaseAction):
    def __init__(self):
        self._description = "Calculate the minimum number of cell phone towers needed to cover all houses."

    def __call__(self, house_positions, radius=4, *args, **kwargs):
        """
        Calculate the minimum number of cell phone towers needed to cover all houses, given that each tower covers a certain radius.

        Args:
            house_positions (dict): A dictionary with keys 'left' and 'right' containing lists of house positions on each side of the road.
            radius (int): The radius (in miles) that each tower covers.

        Returns:
            int: The minimum number of towers needed to cover all houses.
        """
        def min_towers_for_side(houses, radius):
            houses.sort()
            towers = 0
            i = 0
            while i < len(houses):
                tower_loc = houses[i] + radius
                while i < len(houses) and houses[i] <= tower_loc + radius:
                    i += 1
                towers += 1
            return towers

        left_houses = house_positions.get('left', [])
        right_houses = house_positions.get('right', [])
        
        left_towers = min_towers_for_side(left_houses, radius)
        right_towers = min_towers_for_side(right_houses, radius)
        
        total_towers = left_towers + right_towers
        
        print(f"Task execution complete. Minimum number of towers needed: {total_towers}")
        return total_towers

# Example of how to use the class (this should be in the comments):
# tower_calculator = calculate_towers()
# house_positions = {'left': [0, 8, 20], 'right': [0, 11, 24, 29]}
# result = tower_calculator(house_positions=house_positions)

calculate_towers()(house_positions={'left': [7, 15, 27], 'right': [0, 11, 24, 29]})