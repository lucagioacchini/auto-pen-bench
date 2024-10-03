import argparse
from glob import glob
import yaml

# Empty docker-compose
default = {
    'version': '3',
    'networks': {'net-main_network': {'ipam': {'config': [{'subnet': '192.168.0.0/16'}]}}}
}


def create_service(category, task_type, machine_id, oct3, oct4):
    service_name = f'{category}_{task_type}_vm{machine_id}'
    service = {
        'build': f'./{category}/{task_type}/vm{machine_id}',
        'command': 'bash -c "tail -f /dev/null"',
        'container_name': service_name,
        'image': service_name,
        'init': True,
        'restart': 'unless-stopped',
        'tty': True,
        'volumes': [f'./{category}/{task_type}/vm{machine_id}/flag.txt:/root/flag.txt'],
        'networks': {'net-main_network': {'ipv4_address': f'192.168.{oct3}.{oct4}'}}
    }
    return service_name, service


def generate_docker_compose(benchmark, category, task_type, machine_id):
    machine_id = int(machine_id)
    # Extract the third octect of the IP
    categories = glob(f'{benchmark}/machines/*')
    oct_3 = 0
    for cat in categories:
        if 'kali' not in cat:
            oct_3 += len(glob(f'{cat}/*'))

    # Create a new service
    service_name, service = create_service(
        'ctf', 'ac', machine_id, oct_3, machine_id)

    # Assign the new service
    default['services'] = {service_name: service}

    with open(f'{benchmark}/machines/{category}/{task_type}/docker-compose.yml', 'w') as file:
        yaml.dump(default, file, default_flow_style=False)


def update_docker_compose(benchmark, category, task_type, machine_id):
    machine_id = int(machine_id)
    # Extract the third octect of the IP
    with open(
        f'{benchmark}/machines/{category}/{task_type}/docker-compose.yml',
        'r'
    ) as file:
        compose_data = yaml.safe_load(file)
    # Extract existing services
    existing_services = list(compose_data['services'].keys())
    # Get IP address
    existing_address = compose_data['services'][existing_services[0]
                                                ]['networks']['net-main_network']['ipv4_address']
    _, _, oct_3, _ = existing_address.split('.')

    # Create a new service
    service_name, service = create_service(
        'ctf', 'ac', machine_id, oct_3, machine_id)

    # Assign the new service
    compose_data['services'][service_name] = service

    with open(f'{benchmark}/machines/{category}/{task_type}/docker-compose.yml', 'w') as file:
        yaml.dump(compose_data, file, default_flow_style=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Generate a Docker Compose file.')
    parser.add_argument('function', type=str,
                        help='Create or update docker-compose')
    parser.add_argument('benchmark', type=str, help='The benchmark directory')
    parser.add_argument('category', type=str,
                        help='The category of the service')
    parser.add_argument('task_type', type=str,
                        help='The task type of the service')
    parser.add_argument('machine_id', type=str, help='The ID of the machine')

    args = parser.parse_args()

    # Create a new docker-compose
    if args.function == 'create':
        generate_docker_compose(args.benchmark, args.category,
                                args.task_type, args.machine_id)

    # Update a new docker-compose
    elif args.function == 'update':
        update_docker_compose(args.benchmark, args.category,
                              args.task_type, args.machine_id)
