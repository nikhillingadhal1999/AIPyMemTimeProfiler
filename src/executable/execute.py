import sys
from pathlib import Path
import runpy
import os
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT_DIR)
from src.profiler.profile_details import Profiler

def run_with_profiler(filepath, leak_threshold_kb=100):
    filepath = Path(filepath).resolve()
    profiler = Profiler(filepath.parent, leak_threshold_kb=leak_threshold_kb)

    sys.setprofile(profiler.profile_func)
    try:
        runpy.run_path(str(filepath), run_name="__main__")
    finally:
        sys.setprofile(None)
        profiler.write_output()


if __name__ == "__main__":
    # import sys
    # if len(sys.argv) != 2:
    #     print("Usage: python runner.py <script_path>")
    #     sys.exit(1)
    run_with_profiler("/Users/nikhil/code/profiler/test_mem.py")
