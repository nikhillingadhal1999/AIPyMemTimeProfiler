import sys
from pathlib import Path
import runpy
import os
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT_DIR)
from src.config.config import file_path,dir_path,console_display,agentic_profiler
from src.profiler.profile_details import Profiler
from src.flask_app_profiler.load_flask import load_flask_app,wrap_flask_routes
from src.analyser.performance_analyser import analyse_performance,collect_profiling_data
from src.flask_app_profiler.profiler import display_functions_and_select
from rich import print
from rich.console import Console
from rich.table import Table



def run_with_profiler(dirpath,filepath,console_display,leak_threshold_kb=100):
    console = Console()
    app, app_dir = load_flask_app(filepath)
    if app:
        wrap_flask_routes(app, app_dir)
        app.run(debug=True)
        if agentic_profiler:
            profiling_data = collect_profiling_data()
            selected_func = display_functions_and_select(profiling_data)
            if selected_func != None:
                print("\n[Selected] Function:", selected_func[0])
                print("[Selected] File Path:", selected_func[1])
                analyse_result = analyse_performance(selected_func[1],selected_func[0])
                print(analyse_result)
    else:
        filepath = Path(filepath).resolve()
        if console_display == 'False':
            console_display = False
        else:
            console_display = True
        profiler = Profiler(dirpath,console_display,leak_threshold_kb=leak_threshold_kb)
        
        prev_cwd = os.getcwd()
        sys.setprofile(profiler.profile_func)
        print(dir_path)
        os.chdir(dir_path)
        print(file_path)
        sys.path.insert(0, str(dir_path))
        try:
            runpy.run_path(str(filepath), run_name="__main__")
        finally:
            sys.setprofile(None)
            os.chdir(prev_cwd)
            profiler.write_output()
            if agentic_profiler:
                profiling_data = collect_profiling_data()
                selected_func = display_functions_and_select(profiling_data)
                if selected_func != None:
                    print("\n[Selected] Function:", selected_func[0])
                    print("[Selected] File Path:", selected_func[1])
                    analyse_result = analyse_performance(selected_func[1],selected_func[0])
                    print(analyse_result)
            

if __name__ == "__main__":
    run_with_profiler(dir_path,file_path,console_display)