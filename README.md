# Zero-Hassle AI Enabled Python Profiler for Time & Memory

AI enabled lightweight time and memory profiler for Python, zero-configuration python profiler that captures function-level performance metrics along with analysis of function implementation with AI Agent with **no code changes**. Ideal for:

- Python scripts  
- Flask projects  
- Real-time debugging of performance bottlenecks  

---

## Features

### Zero Code Changes
Just run your Python script — no decorators, annotations, or modifications needed.

### Time & Memory Metrics
Automatically captures:
- Max execution time (CPU)
- Peak memory usage
- RSS memory growth
- Return object size
- Arguments passed

### Project-Aware Analysis
Only **your** code is profiled.  
System libraries and external modules are ignored using intelligent project-path detection.

## Profiler Metrics

The following table describes the metrics collected by the profiler:

| **Metric**               | **Description**                                                                                   | **Key**                           |
|--------------------------|---------------------------------------------------------------------------------------------------|-----------------------------------|
| **Function Name**         | The name of the function being profiled.                                                          | `function`                        |
| **File Path**             | The absolute path to the file where the function is defined.                                      | `file`                            |
| **Line Number**           | The line number where the function starts in the file.                                            | `line`                            |
| **Execution Time**        | Maximum time taken by each function in milliseconds (ms).                                         | `max_time_ms`                     |
| **CPU Time**              | Time spent by the CPU on this function (ms).                                                      | `cpu_time_ms`                     |
| **Peak Memory Usage**     | Maximum memory usage during function execution in kilobytes (KB).                                 | `max_mem`                         |
| **RSS Memory Growth**     | Growth in Resident Set Size (RSS) memory in kilobytes (KB), helps spot memory leaks.              | `mem_growth_rss_kb`               |
| **Arguments**             | The arguments passed to the function being profiled.                                              | `args`                            |
| **Possible Memory Leak**  | Indicates if a potential memory leak is detected (if any).                                        | `possible_memory_leak`            |
| **Notes**                 | Any additional notes related to the profiling data.                                               | `note`                            |
| **Returned Object Size**  | The size of the returned object in bytes.                                                         | `return_obj`                      |


Option to select a function for analysis, which is analysed by the Ollama model installed and configured.
This is the table providing the options for analysis.

### Available Functions for Analysis

| **Index** | **Function Name**     | **File Path**                    |
|-----------|------------------------|----------------------------------|
| 0         | `function_one`         | `/path/to/file_one.py`          |
| 1         | `function_two`         | `/path/to/file_two.py`          |
| 2         | `function_three`       | `/path/to/file_three.py`        |
| 3         | `function_four`        | `/path/to/file_four.py`         |
| 4         | `function_five`        | `/path/to/file_five.py`         |
| ...       | ...                    | ...                              |
| N         | `function_n`           | `/path/to/file_n.py`            |
| N+1       | `Skip Analysis`        | `-`                              |


### Structured JSON Reports
Each function includes:
- Function name
- Source file and line number
- Time (ms)
- Memory usage (KB)
- Return object size
- Arguments
- Memory growth & potential leaks

### Works with Any Project Structure
Handles **nested folder hierarchies** easily — just point to your project root and go.

---

## Setup Instructions

### 1. Set Environment Variables

```bash
export PROFILER_FILE_PATH="/absolute/path/to/your_script.py"
export PROFILER_DIR_PATH="/absolute/path/to/your/project/root"
```
If you just want to try, you can test it with sample_project. 
> `export PROFILER_FILE_PATH="$(pwd)/sample_project/inside/app.py"`: The Python file to be profiled  
> `export PROFILER_DIR_PATH="$(pwd)/sample_project/inside"`: Root of your project for accurate filtering

### 2. Optional: Suppress Console Output

By default, profiler prints a table to the console. To disable:

```bash
export CONSOLE_DISPLAY=False
```
## Environment Setup

If you **already have a virtual environment**, just install the dependencies:

```bash
make setup
```

This will install the requirements in your env

If you **don't have a virtual environment**, just install the dependencies:

```bash
make setup
```

This will create an env and install requirements

## LLM Environment Setup

Download Ollama from 
[Ollama](https://ollama.com/)

```bash
ollama run <yout_model>
```
If you don't know which model to use. 
> `ollama run deepseek-r1:1.5b`: It is preferable as it is light weight. 

Set your model env variable.
```bash
export AGENT_NAME="<your_model>"
export AGENTIC_PROFILER=True
```

```bash
make agent-setup
```

To use 

## Run profiler

```bash
make run
```


This will:
- Read the env vars
- Launch your script
- Record memory + execution stats
- Save detailed JSON report

---

## Supported Use Cases

- Pure Python projects
- Flask APIs and apps
- Any directory layout

---

## Want More?

- [ ] Console table toggle
- [ ] HTML report output
- [ ] Jupyter Notebook integration

Pull requests are welcome!
