import sys
import time
import tracemalloc
import json
from pathlib import Path
import os
import gc
from pympler import asizeof
import psutil
import io
from line_profiler import LineProfiler
import re
from rich import print
from rich.console import Console
from rich.table import Table

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT_DIR)
from aipymemtimeprofiler.helpers.helper import check_event, check_external_functions, get_all_args, is_user_code, detect_mem_leak,check_external_lib, get_package
from aipymemtimeprofiler.config.config import file_path, dir_path,INCLUDE_LIBRARIES

class Profiler:
    def __init__(self, root_path,console_display=True, leak_threshold_kb=3000):
        self.root_path = Path(root_path).resolve()
        self.records = {}
        self.call_stack = {}
        self.leak_threshold_kb = leak_threshold_kb
        self.proc = psutil.Process(os.getpid())
        self.console_display = console_display
        self.external_libraries = {}
        tracemalloc.start()

        self.line_profiler = LineProfiler()
        self.line_profiled_functions = set()
        self.line_profiled_output = {}
        self.enable_line_profiling = True

    def profile_func(self, frame, event, arg):
        external_lib = False
        if check_event(event):
            return self.profile_func

        code = frame.f_code
        func_name = code.co_name

        if check_external_functions(func_name,code.co_filename):
            if INCLUDE_LIBRARIES == "True" and check_external_lib(code.co_filename):
                external_lib = True
            else:
                return self.profile_func
                



        # if not is_user_code(frame, self.root_path):
        #     return self.profile_func

        key = (func_name, code.co_filename, frame.f_lineno)

        if event == "call":
            # print("Return call : ",func_name)
            # gc.collect()
            print(f"[CALL] {func_name} at {code.co_filename}")

            all_args = get_all_args(frame)
            key = (func_name, code.co_filename, frame.f_lineno,' '.join(all_args.keys()))
            cpu_start = time.process_time()
            wall_start = time.perf_counter()
            start_snapshot = tracemalloc.take_snapshot()
            mem_start = self.proc.memory_info().rss

            self.call_stack[frame] = {
                "start_time": wall_start,
                "start_cpu": cpu_start,
                "start_snapshot": start_snapshot,
                "args": all_args,
                "mem_start": mem_start
            }

        elif event == "return" and frame in self.call_stack:
            print("Return call : ",func_name)
            all_args = get_all_args(frame)
            key = (func_name, code.co_filename, frame.f_lineno,' '.join(all_args.keys()))
            code_obj = frame.f_code

            if self.enable_line_profiling and code_obj not in self.line_profiled_functions:
                func = frame.f_globals.get(code_obj.co_name)
                if callable(func):
                    self.line_profiler.add_function(func)
                    self.line_profiled_functions.add(code_obj)

            call_info = self.call_stack.pop(frame)
            end_time = time.perf_counter()
            end_cpu = time.process_time()
            mem_end = self.proc.memory_info().rss

            duration = end_time - call_info["start_time"]
            cpu_time = end_cpu - call_info["start_cpu"]
            # print("GC clean : ",func_name)
            # gc.collect()
            end_snapshot = tracemalloc.take_snapshot()
            memory_diff = end_snapshot.compare_to(call_info["start_snapshot"], "lineno")
            total_mem = sum([stat.size_diff for stat in memory_diff])
            max_mem = max([stat.size_diff for stat in memory_diff], default=0)
            mem_growth = mem_end - call_info["mem_start"]

            returned_size = asizeof.asizeof(arg)
            returned_enough = abs(total_mem - returned_size) / 1000
            leak_candidates = detect_mem_leak(memory_diff, self.leak_threshold_kb, self.root_path)

            record = self.records.get(
                key,
                {
                    "function": func_name,
                    "file": code.co_filename,
                    "line": frame.f_lineno,
                    "max_time": 0,
                    "cpu_time": 0,
                    "max_mem": 0,
                    "mem_growth_rss": 0,
                    "mem_growth": 0,
                    "args": call_info["args"],
                    "possible_memory_leak": None,
                    "note": []
                },
            )

            record["max_time"] = max(record["max_time"], duration)
            record["cpu_time"] = max(record["cpu_time"], cpu_time)
            record["max_mem"] = max(record["max_mem"], max_mem)
            record["max_time_ms"] = round(record["max_time"] * 1000, 3)
            record["cpu_time_ms"] = round(record["cpu_time"] * 1000, 3)
            record["max_mem_kb"] = round(record["max_mem"] / 1024, 3)
            record["mem_growth_rss"] = mem_growth
            record["mem_growth_rss_kb"] = max(0,round(mem_growth / 1024, 3))
            record["returned_size"] = returned_size

            if (self.leak_threshold_kb * 1000) < returned_size:
                record["note"].append("Obj return size is huge. Please check.")

            if external_lib:
                self.external_libraries[key] = record
            else:
                self.records[key] = record

        return self.profile_func

    def write_output(self, output_filename="profile_output.json"):
        current_dir = os.getcwd()
        output_file = current_dir+"/profile_output.json"
        
        output = list(self.records.values())
        with open(output_file, "w") as f:
            json.dump(output, f, indent=2)
        
        if self.console_display:
            # print(f"\n[bold green]✅ Profile results written to[/bold green] [cyan]{output_file}[/cyan]")
            console = Console()
            console.rule("[bold yellow]📊 Profiling Summary[/bold yellow]")
            table = Table(show_header=True, header_style="bold magenta", title="Function Profile Overview")
            table.add_column("Function", style="bold cyan")
            table.add_column("Time (ms)", justify="right")
            table.add_column("CPU Time (ms)", justify="right")
            table.add_column("Memory Growth (KB)", justify="right")
            table.add_column("Package", justify="right")
            table.add_column("Note")
            
            output = list(self.external_libraries.values())
            output.extend(list(self.records.values()))

            for record in output:
                note_lines = record.get("note", [])
                if note_lines:
                    note_str = "[bold red]🔴 " + "[/bold red][bright_red]" + "\n      ".join(note_lines) + "[/bright_red]"
                else:
                    note_str = "-"
                if check_external_lib(record['file']):
                    package = get_package(record['file'])
                    table.add_row(
                        record["function"],
                        f"{record['max_time_ms']:.2f}",
                        f"{record['cpu_time_ms']:.2f}",
                        f"{record['mem_growth_rss_kb']:.2f}",
                        package,
                        note_str
                    )
                else:
                    table.add_row(
                        record["function"],
                        f"{record['max_time_ms']:.2f}",
                        f"{record['cpu_time_ms']:.2f}",
                        f"{record['mem_growth_rss_kb']:.2f}",
                        "user_code",
                        note_str
                    )

            console.print(table)
