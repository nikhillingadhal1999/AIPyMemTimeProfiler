import sys
import os
import importlib.util
import time
import psutil
import types
import inspect
from flask import Flask
from memory_profiler import memory_usage
from aipymemtimeprofiler.flask_app_profiler.profiler import flask_profiler,display_functions_and_select
from aipymemtimeprofiler.config.config import agentic_profiler
from aipymemtimeprofiler.analyser.performance_analyser import collect_profiling_data,analyse_performance
import ast

def check_flask_app(filepath):
    with open(filepath, "r") as f:
        tree = ast.parse(f.read(), filename=filepath)

    imports_flask = any(
        isinstance(node, ast.ImportFrom) and node.module == "flask"
        for node in tree.body
    )

    defines_app = any(
        isinstance(node, ast.Assign)
        and any(
            isinstance(target, ast.Name) and target.id == "app"
            for target in node.targets
        )
        for node in tree.body
    )

    return imports_flask and defines_app

def load_flask_app(app_path):
    try:
        if check_flask_app(app_path) == False:
            return None,None
        app_path = os.path.abspath(app_path)
        app_dir = os.path.dirname(app_path)
        module_name = os.path.splitext(os.path.basename(app_path))[0]

        sys.path.insert(0, app_dir)  # allow relative imports
        spec = importlib.util.spec_from_file_location(module_name, app_path)
        module = importlib.util.module_from_spec(spec)  # type: ignore
        sys.modules[module_name] = module
        spec.loader.exec_module(module)  # type: ignore

        for attr in dir(module):
            obj = getattr(module, attr)
            if isinstance(obj, Flask):
                return obj, app_dir
        return None, None
    except Exception as e:
        print(f"Error loading Flask app: {e}")
        return None, None
    # raise Exception("No Flask app found in the given file.")


def wrap_flask_routes(app,dir_path):
    for rule in app.url_map.iter_rules():
        endpoint = app.view_functions[rule.endpoint]
        app.view_functions[rule.endpoint] = wrap_function(endpoint,dir_path)


def wrap_function(func, dir_path):
    def wrapper(*args, **kwargs):
        profiler = flask_profiler()

        # Temporarily change working directory
        prev_dir = os.getcwd()
        os.chdir(dir_path)

        try:
            sys.settrace(profiler.trace_calls)
            mem_used, result = memory_usage((func, args, kwargs), retval=True, max_usage=True, interval=0.01)  # type: ignore
            sys.settrace(None)
            os.chdir(prev_dir)
            profiler.write_output()
        finally:
            os.chdir(prev_dir)

        return result

    wrapper.__name__ = func.__name__
    return wrapper