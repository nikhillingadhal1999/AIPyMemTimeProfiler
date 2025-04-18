import sys
import os
import importlib.util
import time
import psutil
import types
import inspect
from flask import Flask
from memory_profiler import memory_usage
from rich import print
from rich.console import Console
from rich.table import Table
import json
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT_DIR)
from src.helpers.helper import check_external_functions,get_all_args
process = psutil.Process(os.getpid())


class flask_profiler:
    def __init__(self,console_display= False):
        self.records = {}
        self.console_display = console_display

    def trace_calls(self, frame, event, arg):
        if event != "call":
            return

        code = frame.f_code
        filename = code.co_filename
        func_name = code.co_name
        global_vars = frame.f_globals
        used_names = frame.f_code.co_names
        used_globals = {
            name: global_vars[name] for name in used_names if name in global_vars
        }
        
        # Ignore system libs
        if "site-packages" in filename or "lib/python" in filename:
            return
        if check_external_functions(func_name,code.co_filename):
            return

        def local_trace(frame, event, arg,self=self):
            all_args = get_all_args(frame)
            key = (func_name, code.co_filename, frame.f_lineno,' '.join(all_args.keys()))
            if event == "return":
                func = frame.f_globals.get(frame.f_code.co_name)

                start_time = frame.f_locals.get("__start_time__")
                start_cpu = frame.f_locals.get("__start_cpu__")
                start_mem = frame.f_locals.get("__start_mem__")

                if start_time is not None:
                    end_time = time.perf_counter()
                    end_cpu = process.cpu_times().user
                    end_mem = process.memory_info().rss

                    duration = end_time - start_time
                    cpu_time = end_cpu - start_cpu
                    mem_growth = end_mem - start_mem
                    returned_size = sys.getsizeof(arg)
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
                            "args": all_args,
                            "possible_memory_leak": None,
                            "note": []
                        },
                    )
                    record["function"] = func_name
                    record["file"]= filename
                    record["line"] = frame.f_code.co_firstlineno
                    record["max_time"] = duration
                    record["cpu_time"] = cpu_time
                    record["max_time_ms"] = round(duration * 1000, 3)
                    record["cpu_time_ms"]= round(cpu_time * 1000, 3)
                    record["mem_growth_rss"] = mem_growth
                    record["mem_growth_rss_kb"] = round(mem_growth / 1024, 2)
                    record["returned_size"] = returned_size
                    record["possible_memory_leak"]= None
                    record["note"]= (
                                ["Obj return size is huge. Please check."]
                                if returned_size > 10 * 1024 * 1024
                                else []
                            ),
                    record["global_variables"]= used_globals
                    self.records[key] = record
            elif event == "call":
                frame.f_locals["__start_time__"] = time.perf_counter()
                frame.f_locals["__start_cpu__"] = process.cpu_times().user
                frame.f_locals["__start_mem__"] = process.memory_info().rss
            elif event == "exception":
                all_args = get_all_args(frame)
                key = (func_name, code.co_filename, frame.f_lineno,' '.join(all_args.keys()))
                start_time = frame.f_locals.get("__start_time__")
                start_cpu = frame.f_locals.get("__start_cpu__")
                start_mem = frame.f_locals.get("__start_mem__")
                if start_time is not None:
                    end_time = time.perf_counter()
                    end_cpu = process.cpu_times().user
                    end_mem = process.memory_info().rss
                duration = end_time - start_time
                cpu_time = end_cpu - start_cpu
                mem_growth = end_mem - start_mem
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
                        "args": all_args,
                        "possible_memory_leak": None,
                        "note": []
                    },
                )
                record["function"] = func_name
                record["file"]= filename
                record["max_time"]= duration
                record["cpu_time"]= cpu_time
                record["max_time_ms"] = round(duration * 1000, 3)
                record["cpu_time_ms"] = round(cpu_time * 1000, 3)
                record["note"] = ["Exception occoured in this function"]

                self.records[key] = record
            return local_trace

        frame.f_locals["__start_time__"] = time.perf_counter()
        frame.f_locals["__start_cpu__"] = process.cpu_times().user
        frame.f_locals["__start_mem__"] = process.memory_info().rss

        return local_trace
    
    
    def write_output(self, output_file="profile_output.json"):
        def safe_serialize(obj):
            try:
                json.dumps(obj)
                return obj
            except TypeError:
                return str(obj)

        cleaned_records = [
            {k: safe_serialize(v) for k, v in record.items()}
            for record in self.records.values()
        ]

        with open(output_file, "w") as f:
            json.dump(cleaned_records, f, indent=2)

        print(f" Wrote {len(cleaned_records)} records to {output_file}")