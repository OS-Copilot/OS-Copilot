from jarvis.action.base_action import BaseAction
import pandas as pd
import os
from geopy.distance import geodesic

class calculate_adjacent_distances(BaseAction):
    def __init__(self):
        self._description = "Calculate the distances between each pair of adjacent site using latitude and longitude."

    def __call__(self, stations, *args, **kwargs):
        """
        Calculate the distances between each pair of adjacent stations using the geopy library.

        Args:
            stations - A list of tuples, where each tuple contains the name of the station and its coordinates.
                       The format of each tuple is (station_name, (latitude, longitude)).

        
        Returns:
            A list of strings, each describing the distance between a pair of adjacent stations.
            Each string is formatted as "Distance between [Station1] and [Station2]: [distance] km".

        """
        distances = []
        for i in range(len(stations) - 1):
            name1, coords1 = stations[i]
            name2, coords2 = stations[i + 1]
            distance = geodesic(coords1, coords2).kilometers  # Calculating distance using geodesic method
            distances.append(f"Distance between {name1} and {name2}: {distance:.2f} km")
        return distances

# Example of how to use the class (this should be in the comments):
# calculator = calculate_distances()
# stations = [
#     ('Alpha', (40.757707, -73.997332)),
#     ('Beta', (40.817108, -73.958537)),
#     # ... add other stations here
# ]
# distances = calculator(stations)