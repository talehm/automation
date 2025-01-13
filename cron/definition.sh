#!/bin/bash

# Check if arguments are passed
if [ $# -ne 2 ]; then
  echo "Usage: $0 <post_type> <limit>"
  exit 1
fi

# Get the arguments
post_type=$1
limit=$2

# Set the parent directory path explicitly
PARENT_DIR="/home1/jitsrcmy/repositories/automation"

# Source the .env file from the parent directory
if [ -f "$PARENT_DIR/.env" ]; then
  source "$PARENT_DIR/.env"
else
  echo ".env file not found in $PARENT_DIR!"
  exit 1
fi

# Activate virtual environment
source "$PARENT_DIR/venv/Scripts/activate"  # Adjust the path if needed

# Run your Python script with the arguments "post_type" and "limit"
python "$PARENT_DIR/cron/definition.py" "$post_type" "$limit"