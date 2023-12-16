import json

data = {
    'task1' : {
        'name': 'xxx',
        'description': 'xxx',
        'dependencies': ['task2', 'task3']
    }
}

print(data['task1']['dependencies'])
