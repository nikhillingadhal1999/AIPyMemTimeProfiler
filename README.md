# Zero-Hassle AI Enabled Python Profiler for Time, Memory, return object size, cpu memory

AIPyMemTimeProfiler is a zero-configuration, AI-assisted Python profiler that automatically captures function-level memory and time usage — without any code changes.

Powered by LLMs (like Ollama), it not only measures performance but also analyzes your functions for inefficiencies and memory leaks.
---

## Key Features

**Zero code modifications** — No decorators or wrappers needed

**AI-powered analysis** of selected functions

**Function-level** metrics for time, memory, arguments, return object size

**Smart project detection** — Profiles only your code, not external libraries

**Structured JSON output** for automation or visualization

**Optional profiling of third-party libraries**

Supports **Flask apps**, CLI scripts, nested folder hierarchies

### Visualize Performance with Interactive Graphs

AIPyMemTimeProfiler includes a built-in Streamlit dashboard to visualize profiling data in a flamegraph-style format.

What You Get

- Multi-metric overview (time, memory, cpu time, return object size)

- Horizontal flame-style charts

- Interactive tooltips for every function

- No extra config — just run and view


### Installation
    pip install aipymemtimeprofiler

## Quick Start
### 1. Set Environment Variables or pass arguments

```bash
export PROFILER_FILE_PATH="/absolute/path/to/your_script.py"
export PROFILER_DIR_PATH="/absolute/path/to/your/project/root"
```
If you just want to try, you can test it with sample_project. 
> `export PROFILER_FILE_PATH="$(pwd)/sample_project/inside/app.py"`: The Python file to be profiled  
> `export PROFILER_DIR_PATH="$(pwd)/sample_project/inside"`: Root of your project for accurate filtering

### CLI entry point
    profile_code

### OR pass arguments
```bash

profile_code --file-path your_script.py --dir-path /your/output/dir

```

### Arguments 
| Argument                    | Env Variable               | Description                                           | Default                                      |
|----------------------------|----------------------------|-------------------------------------------------------|----------------------------------------------|
| `-h, --help`               | –                          | Show this help message and exit                       | –                                            |
| `--file-path FILE_PATH`    | `PROFILER_FILE_PATH`       | Path to the Python script to profile                  | `None`                                       |
| `--dir-path DIR_PATH`      | `PROFILER_DIR_PATH`        | Working directory and output path                     | `./sample_project/inside`                   |
| `--console-display`        | `CONSOLE_DISPLAY=True`     | Print profiling output to the console                 | `False`                                      |
| `--agentic-profiler`       | `AGENTIC_PROFILER=True`    | Enable AI-based interactive profiling assistant       | `False`                                      |
| `--ollama-model OLLAMA_MODEL` | `AGENT_NAME`            | LLM model name to use with the agentic profiler       | `deepseek-r1:1.5b`                           |
| `--include-libraries`      | `INCLUDE_LIBRARIES=True`   | Include external libraries during profiling           | `False`                                      |
| `--leak-threshold-kb LEAK_THRESHOLD_KB` | –             | Memory leak threshold in KB                           | `10`                                         |

### Launch the Graph UI

```bash
profile_graph
```

### 2. If you want to verify 3rd party libraries

```bash
export INCLUDE_LIBRARIES=True
```

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

### TL;DR
pip install aipymemtimeprofiler
export PROFILER_FILE_PATH=./app.py
export PROFILER_DIR_PATH=./
profile_code

You’ll be prompted to select a function to analyze. Example:

| Index | Function         | File Path                 |
| ----- | ---------------- | ------------------------- |
| 0     | `calculate_data` | `/project/app/compute.py` |
| 1     | `main`           | `/project/app/main.py`    |
| N     | `Skip Analysis`  | -                         |

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
{
  "function": "calculate_total",
  "file": "/app/logic.py",
  "line": 23,
  "cpu_time_ms": 15.3,
  "max_mem": 1024,
  "mem_growth_rss_kb": 300,
  "args": ["x", "y"],
  "return_obj": 124,
  "possible_memory_leak": false,
  "note": ""
}

### Works with Any Project Structure
Handles **nested folder hierarchies** easily — just point to your project root and go.

---

## Supported Use Cases

- Pure Python projects
- Flask APIs and apps
- Any directory layout

---

## Want More?

- [ ] Console table toggle
- [ ] HTML report output

Pull requests are welcome!
