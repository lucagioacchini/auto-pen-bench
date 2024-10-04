import json
import os

from dotenv import load_dotenv
load_dotenv()

# Set environment variables for project and scripts directories
PROJECT = os.environ.get("AUTOPENBENCH")


def load_data(category: str):
    """Load the tasks information nedded by the driver

    Args:
        category (str): in-vitro or real-world

    Returns:
        dict: task information
    """
    with open(f'{PROJECT}/../data/games.json', 'r') as file:
        games = json.loads(file.read())
    return games[category]


def load_milestones(milestone_type: str, level: str, category: str, id: int):
    """Load the command or stage milestones for a given task

    Args:
        milestone_type (str): command or stage
        level (str): the task difficulty level (e.g. in-vitro or real-world)
        category (str): the task category
        id (int): the vulnerable machine identifier

    Returns:
        list: the loaded command or stage milestones
    """
    with open(
        f'{PROJECT}/milestones/{milestone_type}_milestones/{level}/{category}/vm{id}.txt',
        'r'
    ) as file:
        return file.read().split('\n')
