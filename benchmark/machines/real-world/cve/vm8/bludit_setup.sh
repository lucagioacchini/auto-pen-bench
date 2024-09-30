#!/bin/bash

echo "Starting Apache..."
apache2 -D FOREGROUND &

echo "Waiting for Apache to start..."
sleep 5  # Give Apache some time to start

echo "Running Bludit installation script..."
python3 /var/www/html/bludit_install.py

echo "Setup complete. Keeping container alive..."
tail -f /dev/null