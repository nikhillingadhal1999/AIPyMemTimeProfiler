import os
file_path = os.getenv('PROFILER_FILE_PATH','None')
dir_path = os.getenv('PROFILER_DIR_PATH','None')
console_display = os.getenv('CONSOLE_DISPLAY',True)
agentic_profiler = os.getenv('AGENTIC_PROFILER',False)
OLLAMA_MODEL=os.getenv('AGENT_NAME','deepseek-r1:1.5b')
INCLUDE_LIBRARIES = os.getenv('INCLUDE_LIBRARIES',"False")