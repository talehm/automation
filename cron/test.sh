#!/bin/bash

# Check if arguments are passed
if [ $# -ne 2 ]; then
  echo "Usage: $0 <post_type> <soc>"
  exit 1
fi

# Get the arguments
post_type=$1
soc=$2

# Set the parent directory path explicitly

# Source the .env file from the parent directory
if [ -f "../.env" ]; then
  source "../.env"
else
  echo ".env file not found in $PARENT_DIR!"
  exit 1
fi

# Activate virtual environment
source "../venv/Scripts/activate"  # Adjust the path if needed

# Run your Python script with the arguments "post_type" and "soc"
python.exe "social.py" "$post_type" "$soc"