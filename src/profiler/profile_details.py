import sys
import time
import tracemalloc

import json
from pathlib import Path
import runpy
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT_DIR)
from src.helpers.helper import check_event, check_external_functions, get_all_args,is_user_code,detect_mem_leak
from src.config.config import file_path,dir_path

class Profiler:
    def __init__(self, root_path, leak_threshold_kb=100):
        self.root_path = Path(root_path).resolve()
        self.records = {}
        self.call_stack = {}
        self.leak_threshold_kb = leak_threshold_kb
        tracemalloc.start()

    def profile_func(self, frame, event, arg):
        if check_event(event):
            return self.profile_func

        code = frame.f_code
        func_name = code.co_name

        if check_external_functions(func_name):
            return self.profile_func

        if not is_user_code(frame,self.root_path):
            return self.profile_func

        key = (func_name, code.co_filename, frame.f_lineno)

        if not is_user_code(frame,self.root_path):
            return self.profile_func

        if event == "call":
            all_args = get_all_args(frame)
            self.call_stack[frame] = {
                "start_time": time.perf_counter(),
                "start_snapshot": tracemalloc.take_snapshot(),
                "args": all_args,
            }
            print(f"[CALL] {func_name} at {code.co_filename}")
        elif event == "return" and frame in self.call_stack:
            call_info = self.call_stack.pop(frame)
            end_time = time.perf_counter()
            duration = end_time - call_info["start_time"]
            end_snapshot = tracemalloc.take_snapshot()
            memory_diff = end_snapshot.compare_to(call_info["start_snapshot"], "lineno")
            total_mem = sum([stat.size_diff for stat in memory_diff])
            max_mem = max([stat.size_diff for stat in memory_diff], default=0)

            # Collect high memory diff lines from user code
            leak_candidates = detect_mem_leak(memory_diff,self.leak_threshold_kb,self.root_path)

            record = self.records.get(
                key,
                {
                    "function": func_name,
                    "file": code.co_filename,
                    "line": frame.f_lineno,
                    "max_time": 0,
                    "max_mem": 0,
                    "mem_not_freed": 0,
                    "args": call_info["args"],
                    "possible_memory_leak": None,
                },
            )

            record["max_time"] = max(record["max_time"], duration)
            record["max_mem"] = max(record["max_mem"], max_mem)
            record["max_time_ms"] = round(record["max_time"] * 1000, 3)
            record["max_mem_kb"] = round(record["max_mem"] / 1024, 3)
            record["mem_not_freed"] += total_mem
            record["mem_not_freed_kb"] = round(record["mem_not_freed"] / 1024, 3)

            if leak_candidates:
                record["possible_memory_leak"] = leak_candidates

            self.records[key] = record

        return self.profile_func

    def write_output(self, output_file="profile_output.json"):
        output = list(self.records.values())
        with open(output_file, "w") as f:
            json.dump(output, f, indent=2)
        print(f"\n Profile results written to {output_file}")