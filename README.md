# PyMemTimeProfiler
Zero-Hassle Python Profiler for Time & Memory — No Code Changes Needed
Debugging performance issues in Python shouldn't be a chore. This lightweight profiler tracks function-level memory usage and execution time across your codebase — no decorators, no annotations, and no code changes required. Perfect for debugging performance issues real-time. 

***Features***
* **Zero Code Changes**

    Just run your Python script — no need to decorate or modify functions.

* **Time & Memory Metrics**

    Automatically captures the maximum execution time (wall & CPU) and peak memory usage for each function, including RSS memory growth.

* **Project-Aware Analysis**

    Only your application code is profiled — system libraries and external modules are automatically ignored using project path detection.

* **Structured JSON Reports**

    Detailed per-function stats: function name, file, line number, time (ms), memory usage (KB), return object size and arguments. 

* **Execution Time Tracking**

    Records max time taken by each function.

* **Works with Any Project Structure**

    Handles arbitrary folder hierarchies — just point to your project root.

***What You'll Get***

* Execution time tracking (ms)

* Peak memory usage (KB)

* Returned object size (bytes)

* Growth in RSS memory (KB)

* Function-level granularity



***Setup Environment Variables***

Before running the profiler, make sure to set the following environment variables:

* ```export PROFILER_FILE_PATH="/absolute/path/to/your/python_script.py"```
* ```export PROFILER_DIR_PATH=="/absolute/path/to/your/project/root"```
* ```python3 install -m venv env```
* ```pip3 install -r requirements.txt```

* FILE_PATH: The absolute path to the Python script you want to profile.```

* DIR_PATH: The absolute path to your project directory. This helps the profiler focus only on your application code and ignore system/internal Python calls.

***Running the Profiler***

  After setting the environment variables, simply run the profiler using the provided shell script:

* ```./run_profiler.sh```
  This script reads the environment variables FILE_PATH and DIR_PATH, launches your script, and records the memory and execution time statistics for each function without requiring any code changes or decorators.
