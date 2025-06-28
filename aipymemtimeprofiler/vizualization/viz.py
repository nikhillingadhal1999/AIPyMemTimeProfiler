import subprocess
from pathlib import Path

def main():
    app_script = Path(__file__).parent / "graph.py"
    subprocess.run(["streamlit", "run", str(app_script)])

if __name__ == "__main__":
    main()