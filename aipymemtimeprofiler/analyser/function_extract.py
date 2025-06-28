import ast
import textwrap

def extract_function_from_file(file_path: str, function_name: str) -> str:
    with open(file_path, 'r') as f:
        source = f.read()

    parsed_ast = ast.parse(source)
    for node in ast.walk(parsed_ast):
        if isinstance(node, ast.FunctionDef) and node.name == function_name:
            lines = source.splitlines()
            start_line = node.lineno - 1
            end_line = node.end_lineno
            func_lines = lines[start_line:end_line]
            return textwrap.dedent("\n".join(func_lines))

    raise ValueError(f"Function '{function_name}' not found in {file_path}")
