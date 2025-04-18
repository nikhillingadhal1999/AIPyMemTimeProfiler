import sys
import os
import importlib.util
import time
import psutil
import types
import inspect
from flask import Flask
from memory_profiler import memory_usage
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT_DIR)
from src.flask_app_profiler.profiler import flask_profiler
from src.config.config import file_path, dir_path

def load_flask_app(app_path):
    try:
        module_name = os.path.splitext(os.path.basename(app_path))[0]

        spec = importlib.util.spec_from_file_location(module_name, app_path)
        module = importlib.util.module_from_spec(spec) # type: ignore
        sys.modules[module_name] = module
        spec.loader.exec_module(module) # type: ignore
        for attr in dir(module):
            obj = getattr(module, attr)
            if isinstance(obj, Flask):
                return obj
        return None
    except:
        return None
    # raise Exception("No Flask app found in the given file.")


def wrap_flask_routes(app):
    for rule in app.url_map.iter_rules():
        endpoint = app.view_functions[rule.endpoint]
        app.view_functions[rule.endpoint] = wrap_function(endpoint)


def wrap_function(func):
    def wrapper(*args, **kwargs):
        profiler = flask_profiler()
        sys.settrace(profiler.trace_calls)
        mem_used, result = memory_usage((func, args, kwargs), retval=True, max_usage=True, interval=0.01) # type: ignore
        sys.settrace(None)
        profiler.write_output()
        return result

    wrapper.__name__ = func.__name__
    return wrapper