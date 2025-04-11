# # test_script.py

# import time

# global_list = []

# def fast_function():
#     return sum(i for i in range(1000))

# def slow_function():
#     time.sleep(0.1)
#     return [x ** 2 for x in range(1000)]

# def leaky_function():
#     # Simulate a memory leak by appending to a global list
#     for _ in range(100):
#         global_list.append('x' * 10000)  # ~1MB per 100 appends

# def main():
#     fast_function()
#     slow_function()
#     leaky_function()
#     fast_function()
#     slow_function()


# main()

def leaky_func():
    big_data = [x for x in range(10**6)]  # ~8MB if ints
    return big_data


def main():
    leaky_func()

main()