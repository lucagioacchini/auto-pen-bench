from autopenbench.driver import PentestDriver
from autopenbench.tools import *
from autopenbench.utils import load_data
from termcolor import cprint
import sys
import time
import re

INVITRO = 'benchmark/machines/in-vitro'


def extract_content(target: str, cmd: str = ''):
    """Extract the content of the solutions from the provided action.

    Args:
        target (str): task name
        cmd (str, optional): command pointing to the content to extract. 
        Defaults to ''.

    Returns:
        str: the extracted content
    """
    if target == 'real-world_cve_vm4':
        pattern = r"/root/\.msf4/loot/(.*)\.bin"
        match = re.search(pattern, cmd)
        content = match.group(1)
    elif target == 'real-world_cve_vm5':
        pattern = r"/root/\.msf4/loot/(.*)\.txt"
        match = re.search(pattern, cmd)
        content = match.group(1)
    elif target == 'in-vitro_network_security_vm4':
        with open(f'{INVITRO}/network_security/vm4/solution.py', 'r') as file:
            content = file.read()
    elif target == 'in-vitro_network_security_vm5':
        with open(f'{INVITRO}/network_security/vm5a/solution.py', 'r') as file:
            content = file.read()
    elif target == 'in-vitro_cryptography_vm2':
        with open(f'{INVITRO}/cryptography/vm2/solution.py', 'r') as file:
            content = file.read()
    elif target == 'in-vitro_cryptography_vm3':
        with open(f'{INVITRO}/cryptography/vm3/solution.py', 'r') as file:
            content = file.read()
    return content


# Check if all the parameters are provided as command-line arguments
if len(sys.argv) != 4:
    print("Usage: python3 machine_test.py <LEVEL> <CATEGORY> <GAME_ID>")
    sys.exit(1)

# Get arguments from command-line argument
LEVEL = sys.argv[1]  # in-vitro or real-world
CATEGORY = sys.argv[2]  # task category
GAME_ID = int(sys.argv[3])  # vm identifier
SOLUTIONS = f'benchmark/solutions/{LEVEL}/{CATEGORY}'  # Solutions path

# Load the vulnerable machine to test
game = load_data(LEVEL)[CATEGORY][GAME_ID]

# Load solutions
with open(f'{SOLUTIONS}/vm{GAME_ID}.txt', 'r') as file:
    solutions = file.readlines()

# Initialize the driver and reset
driver = PentestDriver(game['task'], game['flag'], game['target'])
driver.reset()

# Perform the solutions in sequence
for step, solution in enumerate(solutions):
    # Extract the dynamically created file name for network_security_vm4 and
    # vm5 and cryptography vm2 and vm3
    if game['target'] == 'in-vitro_network_security_vm4' and step == 0:
        fname = extract_content(game['target'])
    if game['target'] == 'in-vitro_network_security_vm5' and step == 0:
        fname = extract_content(game['target'])
    elif game['target'] == 'in-vitro_cryptography_vm2' and step == 5:
        fname = extract_content(game['target'])
    elif game['target'] == 'in-vitro_cryptography_vm3' and step == 5:
        fname = extract_content(game['target'])

    # Create the action
    action = eval(solution)
    time.sleep(.5)
    cprint(f'ACTION: {solution}', 'yellow')

    # Perform the step
    observation, done = driver.step(action)
    time.sleep(.5)

    # Extract the dynamically created file name for real-world_cve_vm4 and vm5
    if game['target'] == 'real-world_cve_vm4' and step == 11:
        fname = extract_content(game['target'], observation)
    if game['target'] == 'real-world_cve_vm5' and step == 8:
        fname = extract_content(game['target'], observation)

    # Print the observation
    cprint(f'OBSERVATION: {observation}\n', 'cyan')
