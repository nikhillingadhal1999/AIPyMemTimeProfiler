import os
file_path = os.getenv('PROFILER_FILE_PATH','None')
dir_path = os.getenv('PROFILER_DIR_PATH','None')
console_display = os.getenv('CONSOLE_DISPLAY',True)
agentic_profiler = os.getenv('AGENTIC_PROFILER',False)
# have a seperate folder and all project in that. Don't include the env in that folder.