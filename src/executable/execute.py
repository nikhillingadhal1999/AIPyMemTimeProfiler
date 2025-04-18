import sys
from pathlib import Path
import runpy
import os
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT_DIR)
from src.config.config import file_path,dir_path,console_display
from src.profiler.profile_details import Profiler
from src.flask_app_profiler.load_flask import load_flask_app,wrap_flask_routes

def run_with_profiler(filepath,console_display,leak_threshold_kb=100):
    app = load_flask_app(filepath)
    if app != None:
        wrap_flask_routes(app)
        app.run(debug=True)
    else:
        filepath = Path(filepath).resolve()
        if console_display == 'False':
            console_display = False
        else:
            console_display = True
        profiler = Profiler(dir_path,console_display,leak_threshold_kb=leak_threshold_kb)
        
        prev_cwd = os.getcwd()
        sys.setprofile(profiler.profile_func)
        print(dir_path)
        os.chdir(dir_path)
        sys.path.insert(0, str(dir_path))
        try:
            runpy.run_path(str(filepath), run_name="__main__")
        finally:
            sys.setprofile(None)
            os.chdir(prev_cwd)
            profiler.write_output()

if __name__ == "__main__":
    run_with_profiler(file_path,console_display)