#!/bin/bash

# Function to check if a command is available
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Install pip3 package in editable mode
pip3 install -e .

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

# Navigate to benchmark directory and set environment variable
cd benchmark
echo "AUTOPENBENCH=$(pwd)" > ../.env
echo "KALISCRIPTS=$(pwd)/machines/kali/tmp_script" >> ../.env

# Build and start Docker containers
docker-compose -f docker-compose.yml \
               -f machines/in-vitro/access_control/docker-compose.yml \
               -f machines/in-vitro/web_security/docker-compose.yml \
               -f machines/in-vitro/network_security/docker-compose.yml \
               -f machines/in-vitro/cryptography/docker-compose.yml \
               -f machines/real-world/cve/docker-compose.yml \
                build

cd ..