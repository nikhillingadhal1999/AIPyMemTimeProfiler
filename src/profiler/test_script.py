from test1 import helper_function,leaky_function,slow_function
def core_function(a, b):
    res1 = helper_function(a)
    leaky_function(100000)  # consume and leak memory
    res2 = slow_function(b)
    return res1 + res2

def main():
    for i in range(2):  # Run it multiple times to generate trace data
        core_function(i + 1, 500)

if __name__ == '__main__':
    main()