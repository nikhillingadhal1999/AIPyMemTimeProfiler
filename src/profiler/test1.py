import time

leaky_list = []  # global list to simulate memory leak

def slow_function(n):
    total = 0
    for i in range(n):
        for j in range(1000):  # nested loop to consume time
            total += (i * j) % 7
    return total

def leaky_function(size):
    data = [i for i in range(size)]  # large list in local scope
    leaky_list.append(data)  # reference kept globally — memory leak

def helper_function(x):
    time.sleep(0.1)  # simulate delay
    return x * x
