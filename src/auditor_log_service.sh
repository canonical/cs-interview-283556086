#!/bin/zsh

# Install required packages
sudo apt-get update
sudo apt-get install -y python3 python3-pip sqlite3

# Create the database
sqlite3 events.db ""

# Start the service
python3 auditor_server_launcher.py