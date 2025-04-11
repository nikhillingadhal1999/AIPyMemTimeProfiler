# PyMemTimeProfiler
A no-hassle Python memory & time profiler that detects potential memory leaks — without touching your code.
It is a zero-setup Python profiler that tracks memory usage, detects potential memory leaks, and measures execution time for every function — no code changes required. Perfect for debugging performance issues and spotting leaks in real-time.

Zero Code Changes – Just run your script, no decorators or annotations needed.
Memory Leak Detection – Automatically spots potential leaks with realistic thresholds.
Execution Time Tracking – Records max time taken by each function.
Detailed Reporting – Generates a JSON report with function names, memory usage, line numbers, and arguments.
Ignores Non-User Code – Only tracks files in your project, excluding system/internal calls.
Supports Any Project Structure – Works with custom folder hierarchies using dynamic path resolution.

***Setup Environment Variables***

Before running the profiler, make sure to set the following environment variables:

export PROFILER_FILE_PATH="/absolute/path/to/your/python_script.py"

export PROFILER_DIR_PATH=="/absolute/path/to/your/project/root"

FILE_PATH: The absolute path to the Python script you want to profile.

DIR_PATH: The absolute path to your project directory. This helps the profiler focus only on your application code and ignore system/internal Python calls.

***Running the Profiler***

After setting the environment variables, simply run the profiler using the provided shell script:

./run_profiler.sh
This script reads the environment variables FILE_PATH and DIR_PATH, launches your script, and records the memory and execution time statistics for each function without requiring any code changes or decorators.
