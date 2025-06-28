import inspect
from pathlib import Path


def check_event(event):
    return event not in ("call", "return")


def check_external_functions(func_name,file_name):
    return (
        func_name.startswith("<") and func_name.endswith(">")
    ) or "<frozen importlib._bootstrap>" in file_name or "site-packages" in file_name or "lib/python" in file_name or (file_name.startswith("<") and file_name.endswith(">"))

def check_external_lib(file_name):
    return "site-packages" in file_name

def get_package(file_name):
    return file_name.split("site-packages")[1].split("/")[1]

def get_all_args(frame):
    args_info = inspect.getargvalues(frame)
    args_repr = {}
    for k in args_info.args:
        try:
            args_repr[k] = repr(args_info.locals[k])
        except Exception:
            args_repr[k] = "<unrepresentable>"
    return args_repr


def is_user_code(frame_or_path, root_path):
    file_path = Path(
        frame_or_path.f_code.co_filename
        if hasattr(frame_or_path, "f_code")
        else frame_or_path
    ).resolve()
    return str(file_path).startswith(str(root_path))


def detect_mem_leak(memory_diff, leak_threshold_kb, root_path):
    leak_candidates = []
    for stat in memory_diff:
        size_kb = stat.size_diff / 1024
        if (
            stat.size_diff > 0
            and is_user_code(stat.traceback[0].filename, root_path)
            and size_kb >= leak_threshold_kb
        ):
            leak_candidates.append(
                {
                    "file": str(Path(stat.traceback[0].filename).resolve()),
                    "line": stat.traceback[0].lineno,
                    "size_kb": round(size_kb, 3),
                }
            )
    return leak_candidates