#!/bin/bash
set -x  # Enable debugging output

# Get the directory where this script resides
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Set PYTHONPATH to include the 'backend' directory
export PYTHONPATH="${SCRIPT_DIR}:${PYTHONPATH}"

# Load environment variables from .env file in the script directory
ENV_FILE="${SCRIPT_DIR}/.env"
if [[ -f "$ENV_FILE" ]]; then
    while IFS= read -r line; do
        # Ignore lines starting with '#' (comments) and empty lines
        if [[ "$line" =~ ^\s*# ]] || [[ -z "$line" ]]; then
            continue
        fi
        # Export variable and its value
        export "$line"
    done < "$ENV_FILE"
else
    echo "$ENV_FILE file not found."
    exit 1
fi

# Check if running in Docker
if [[ ! -z "${DOCKER_ENV}" ]]; then
    # Running in Docker, set host to 0.0.0.0
    HOST="0.0.0.0"
else
    # Not running in Docker, use localhost as default host
    HOST="localhost"
fi


# Let the DB start
python "${SCRIPT_DIR}/backend_pre_start.py"

# Create initial data in DB
python "${SCRIPT_DIR}/initial_data.py"

# Start your application
uvicorn backend.app:app --host "${HOST}" --reload
