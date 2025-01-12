#!/bin/bash

# Source the .env file to export variables into the current shell session
source .env
./venv/Scripts/activate
# Now you can run your Python script or any other command with the environment variables loaded
python cron/social.py "definition" "threads"