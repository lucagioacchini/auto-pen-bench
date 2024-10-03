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
