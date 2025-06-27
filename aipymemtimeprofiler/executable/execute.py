import sys
from pathlib import Path
import runpy
import os
import aipymemtimeprofiler.config.config as config
from aipymemtimeprofiler.profiler.profile_details import Profiler
from aipymemtimeprofiler.flask_app_profiler.load_flask import load_flask_app,wrap_flask_routes
from aipymemtimeprofiler.analyser.performance_analyser import analyse_performance,collect_profiling_data
from aipymemtimeprofiler.flask_app_profiler.profiler import display_functions_and_select
from rich import print
from rich.console import Console
from rich.table import Table
import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        description="AIPyMemTimeProfiler: Profile Python code with time & memory insights.\n"
                    "Prioritizes command-line arguments. Falls back to environment variables.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "--file-path", type=str,
        help="Path to the Python script you want to profile. (or set ENV: PROFILER_FILE_PATH)"
    )
    parser.add_argument(
        "--dir-path", type=str,
        help="Working directory for the script and where output will be saved. (or set ENV: PROFILER_DIR_PATH)",
        default=os.getenv("PROFILER_DIR_PATH", os.getcwd())
    )
    parser.add_argument(
        "--console-display", action="store_true",
        help="Print profiling output to the console. (or set ENV: CONSOLE_DISPLAY=True)"
    )
    parser.add_argument(
        "--agentic-profiler", action="store_true",
        help="Enable interactive AI-based profiling assistant. (or set ENV: AGENTIC_PROFILER=True)"
    )
    parser.add_argument(
        "--ollama-model", type=str,
        help="LLM model name to use with the agentic profiler. (or set ENV: AGENT_NAME)",
        default=os.getenv("AGENT_NAME", "deepseek-r1:1.5b")
    )
    parser.add_argument(
        "--include-libraries", action="store_true",
        help="Include external libraries in profiling. (or set ENV: INCLUDE_LIBRARIES=True)"
    )
    parser.add_argument(
        "--leak-threshold-kb", type=int, default=10,
        help="Memory leak threshold in KB. (default: 10 KB)"
    )

    return parser.parse_args()



def run_with_profiler():
    args = parse_args()
    file_path = args.file_path or os.getenv("PROFILER_FILE_PATH")
    dir_path = args.dir_path or os.getenv("PROFILER_DIR_PATH", os.getcwd())
    console_display = args.console_display or os.getenv("CONSOLE_DISPLAY", "False") == "True"
    agentic_profiler = args.agentic_profiler or os.getenv("AGENTIC_PROFILER", "False") == "True"
    config.ollama_model = args.ollama_model or os.getenv("AGENT_NAME", "deepseek-r1:1.5b")
    config.include_libraries = args.include_libraries or os.getenv("INCLUDE_LIBRARIES", "False") == "True"
    leak_threshold_kb = args.leak_threshold_kb
    console = Console()
    app, app_dir = load_flask_app(file_path)
    if app:
        wrap_flask_routes(app, app_dir)
        app.run(debug=True)
        if agentic_profiler == True:
            profiling_data = collect_profiling_data()
            selected_func = display_functions_and_select(profiling_data)
            if selected_func != None:
                print("\n[Selected] Function:", selected_func[0])
                print("[Selected] File Path:", selected_func[1])
                analyse_result = analyse_performance(selected_func[1],selected_func[0])
                print(analyse_result)
    else:
        filepath = Path(file_path).resolve()
        console_display= True
        if console_display == 'False':
            console_display = False
        else:
            console_display = True
        profiler = Profiler(dir_path,console_display,leak_threshold_kb=leak_threshold_kb)
        
        prev_cwd = os.getcwd()
        sys.setprofile(profiler.profile_func)
        print(dir_path)
        os.chdir(dir_path)
        print(file_path)
        sys.path.insert(0, str(dir_path))
        try:
            # print("Running..",filepath)
            runpy.run_path(str(filepath), run_name="__main__")
        finally:
            sys.setprofile(None)
            os.chdir(prev_cwd)
            profiler.write_output()
            print("ENABLE AI : ",agentic_profiler)
            print(agentic_profiler==True)
            if agentic_profiler == True:
                profiling_data = collect_profiling_data()
                while(1):
                    selected_func = display_functions_and_select(profiling_data)
                    if selected_func != None:
                        print("\n[Selected] Function:", selected_func[0])
                        print("[Selected] File Path:", selected_func[1])
                        analyse_result = analyse_performance(selected_func[1],selected_func[0])
                        print(analyse_result)
                    else:
                        exit(0)
            

if __name__ == "__main__":
    run_with_profiler()