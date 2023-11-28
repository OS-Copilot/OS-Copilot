from itertools import permutations
cities = {'Hangzhou': 1, 'Shanghai': 3, 'Wuhan': 3, 'Chengdu': 1}
city_permutations = permutations(cities.keys())
best_sequence = None
min_days_spent = float('inf')
for perm in city_permutations:
    days_spent = sum(cities[city] for city in perm)
    if days_spent < min_days_spent:
        min_days_spent = days_spent
        best_sequence = perm
print(f'Best sequence: {best_sequence}')
print(f'Minimum days spent: {min_days_spent}')
