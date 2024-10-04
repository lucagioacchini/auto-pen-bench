#!/bin/bash

# Function to check if a command is available
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if Docker is installed; if not, install it
if ! command_exists docker; then
    echo "Installing Docker..."
    sudo apt update
    sudo apt install -y docker.io
fi

# Check if Docker Compose is installed; if not, install it
if ! command_exists docker-compose; then
    echo "Installing Docker Compose..."
    sudo apt update
    sudo apt install -y docker-compose
fi

mkdir benchmark/machines/kali/tmp_script

echo "AUTOPENBENCH=$(pwd)/benchmark" > .env
echo "KALISCRIPTS=$(pwd)/benchmark/machines/kali/tmp_script" >> .env

pip3 install -e .