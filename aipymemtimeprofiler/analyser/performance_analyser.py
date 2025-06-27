import ollama
import json
import os
import re
import sys
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT_DIR)
from aipymemtimeprofiler.analyser.function_extract import extract_function_from_file
from aipymemtimeprofiler.config.config import OLLAMA_MODEL


def connect_to_ollama():
    return ollama

def remove_think_blocks(text):
    text = text.split("content=")[1]
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)

# Step 2 (Optional): Make **bold** sections uppercase or add console colors
def emphasize_bold(text):
    return re.sub(r"\*\*(.*?)\*\*", lambda m: m.group(1).upper(), text)

def send_analysis_request(code):
    client = connect_to_ollama()
    prompt = f"""
        You are a Python programming expert.
        You have a keen eye for unused variables, memory and time optimization.
        Ignore the imports. Assume we have proper imports to the function
        Given the following Python code in section __code__ , your task is to analyse the code deeply check if there are absolutely necessary variables be careful while doing this think twice:
        1. **Identify any errors** (e.g., syntax errors, logical mistakes, potential runtime errors).
        2. **Find inefficiencies** in the code (e.g., unnecessary computations, inefficient algorithms, redundant operations).
        3. **Suggest improvements** to fix the errors and optimize the code. Your suggestions should focus on:
            - Correcting any errors.
            - Improving efficiency (both in terms of time and memory).
            - Refactoring the code for better readability and maintainability.
            - Following Python best practices (e.g., variable naming, code style according to PEP 8).
            - Any other performance optimizations or recommendations.
            - Check if there are any unused variables in the code. If there are it's a possible memory leak
            - Check the unused variables twice. Think about this.
            - If there are any global variables used. Warn that global variables are used in this function.

        Do not provide any extra explanation or commentary beyond the identification and suggestions.
        Print only short answers. Give only Analysis and suggested code
        If you don't have any important problems. Then say Everything looks good and don't suggest anything.
        ****problem and analysis****
        Write the problems found and analysis here

        ****suggested_code****
        Suggested code here

        Here is the code to analyze:
        __code__
        {code}
        """
    response = client.chat(model=OLLAMA_MODEL, messages=[{"role": "user", "content": prompt}])
    response = remove_think_blocks(str(response))
    formatted_content = response.encode().decode('unicode_escape')
    readable_output = emphasize_bold(formatted_content)

    # print("Full Response:", response,type(response))

    try:
        return readable_output
    except json.JSONDecodeError:
        print("Failed to return content:", response)
        return None



def collect_profiling_data():
    current_dir = os.getcwd()
    file_path = current_dir + "/profile_output.json"
    
    if not os.path.exists(file_path):
        print(f"Error: File not found at path '{file_path}'")
        return []

    try:
        with open(file_path, "r") as f:
            profiling_data = json.load(f)

            if not isinstance(profiling_data, list):
                print("Error: JSON root should be a list of profiling entries.")
                return []

            # Extract only (function, file) as a list of tuples
            return [(entry["function"], entry["file"]) for entry in profiling_data if "function" in entry and "file" in entry]

    except json.JSONDecodeError:
        print("Error: Failed to decode JSON.")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []



def analyze_performance(profiling_function):
    analysis_results = send_analysis_request(profiling_function)
    
    if analysis_results:
        return analysis_results
    else:
        print("No analysis results returned.")
        return None

def analyse_performance(function_file,function_name):
    code = extract_function_from_file(function_file,function_name)
    print("Analysing code \n", code)
    analysis_results = analyze_performance(code)
    print("Analysis completed")
    return analysis_results