# Define the environment variables
ENV_NAME = env
REQUIREMENTS_FILE = $(shell pwd)/requirements.txt
AGENT_REQUIREMENTS_FILE = $(shell pwd)/agent_requirements.txt

# Define the current working directory and executable path
CURRENT_DIR := $(shell pwd)
EXECUTE_PATH := $(CURRENT_DIR)/aipymemtimeprofiler/executable/execute.py

setup:
	@if [ ! -d "$(ENV_NAME)" ]; then \
		python3 -m venv $(ENV_NAME); \
		echo "Virtual environment created."; \
	fi
	@echo "Installing dependencies into virtual environment..."
	@source $(ENV_NAME)/bin/activate && pip install -r $(REQUIREMENTS_FILE)

agent-setup:
	@if [ ! -d "$(ENV_NAME)" ]; then \
		python3 -m venv $(ENV_NAME); \
		echo "Virtual environment created."; \
	fi
	@echo "Installing agent dependencies into virtual environment..."
	@source $(ENV_NAME)/bin/activate && pip install -r $(AGENT_REQUIREMENTS_FILE)

run:
	@echo "Checking if PROFILER_FILE_PATH and PROFILER_DIR_PATH environment variables are set..."
	@if [ -z "$$PROFILER_FILE_PATH" ] || [ -z "$$PROFILER_DIR_PATH" ]; then \
		echo "Error: PROFILER_FILE_PATH or PROFILER_DIR_PATH environment variables are not set."; \
		echo "Please set them as follows:"; \
		echo '  export PROFILER_FILE_PATH="/absolute/path/to/your/script.py"'; \
		echo '  export PROFILER_DIR_PATH="/absolute/path/to/your/project"'; \
		exit 1; \
	fi
	@echo "Running profiler with script at $(EXECUTE_PATH)"
	@source $(ENV_NAME)/bin/activate && python3 $(EXECUTE_PATH)

clean:
	rm -rf $(ENV_NAME)
	rm -f profile_output.json
