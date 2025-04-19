python3 src/executable/execute.py

#!/bin/bash

ENV_NAME="env"
REQUIREMENTS_FILE="requirements.txt"

if [ -d "$ENV_NAME" ]; then
    echo "Virtual environment found. Activating..."
    source "$ENV_NAME/bin/activate"
else
    echo "Virtual environment not found. Creating new one..."
    python3 -m venv "$ENV_NAME"
    source "$ENV_NAME/bin/activate"
    echo "Installing required packages..."
    pip install -r "$REQUIREMENTS_FILE"
fi

if [ -z "$PROFILER_FILE_PATH" ] || [ -z "$PROFILER_DIR_PATH" ]; then
    echo "Error: PROFILER_FILE_PATH or PROFILER_DIR_PATH environment variables are not set."
    exit 1
fi

echo "Running profiler on $PROFILER_FILE_PATH..."
python3 -m profiler

deactivate
