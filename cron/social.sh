#!/bin/bash

# Check if arguments are passed
if [ $# -ne 2 ]; then
  echo "Usage: $0 <post_type> <soc>"
  exit 1
fi

# Get the arguments
post_type=$1
soc=$2

# Source the .env file from the parent directory
if [ -f .env ]; then
  source .env
else
  echo ".env file not found in the parent directory!"
  exit 1
fi

# Activate virtual environment
source ./venv/Scripts/activate  # Adjust the path if needed

# Run your Python script with the arguments "post_type" and "soc"
python cron/social.py "$post_type" "$soc"