import argparse
import json


def update_data(category, task_type, machine_id):
    with open('data/games.json', 'r') as file:
        data = json.loads(file.read())

    if category not in data:
        data[category] = {}
    if task_type not in data[category]:
        data[category][task_type] = []

    obj = {
        "task": "WRITE YOUR TASK PROMPT HERE",
        "flag": "WRITE YOUR FLAG HERE",
        "target": f"{category}_{task_type}_vm{machine_id}",
        "vulnerability": "DESCRIBE YOUR VULNERABILITY HERE"
    }
    data[category][task_type].append(obj)

    with open('data/games2.json', 'w') as file:
        file.write(json.dumps(data))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Update the input data Json file.')
    parser.add_argument('category', type=str,
                        help='The category of the service')
    parser.add_argument('task_type', type=str,
                        help='The task type of the service')
    parser.add_argument('machine_id', type=str, help='The ID of the machine')

    args = parser.parse_args()

    update_data(args.category, args.task_type, args.machine_id)
