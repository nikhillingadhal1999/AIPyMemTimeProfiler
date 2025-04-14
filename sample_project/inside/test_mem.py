
# def main():
#     fast_function()
#     slow_function()
#     leaky_function()
#     fast_function()
#     slow_function()


# main()
from rich import print
from rich.console import Console
from test_folder.test_1 import fast_function,leaky_function,slow_function
def pretty_print_message():
    console = Console()
    console.rule("[bold blue]🚀 Welcome to the Profiler!")
    print("[green]Everything is running smoothly.[/green] ✅")
    console.rule("[bold blue]Profiler End[/bold blue]")

def leaky_func():
    big_data = [x for x in range(10**6)]  # ~8MB if ints
    return big_data

def read_file():
    with open('test.txt') as f:
        print(f.readlines())

def main():
    leaky_func()
    pretty_print_message()
    fast_function()
    slow_function()
    leaky_function()
    fast_function()
    slow_function()
    read_file()


main()