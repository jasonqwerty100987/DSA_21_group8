import nqueen as nq
import time as time
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors as c
from matplotlib.pyplot import figure
import statistics
import pandas as pd
import sys
import copy

def print_solution(solution, n, title, time, i):
    result = [[0 if i%2 == 0 else 1 for i in range(n)] if j%2 == 0 else [1 if i%2 == 0 else 0 for i in range(n)] for j in range(n)]
    for index, key in enumerate(solution):
        result[key - 1][index] = 2


    figure(i, figsize=(5, 5), dpi=250)
    x = np.arange(0, n + 1, 1)  # len = 10
    y = np.arange(0, n + 1, 1)  # len = 10
    cMap = c.ListedColormap(['white', 'gray', 'skyblue'])
    plt.pcolormesh(x, y, result, cmap=cMap)
    plt.xticks(np.arange(0, n+1, 1.0))
    plt.yticks(np.arange(0, n+1, 1.0))
    plt.title(title + " " + str(time)+" seconds")
    plt.grid()

def direct_compare(n):
    result = []
    print("n = {}".format(n))
    print(nq.get_random_state(n))
    print("Using Hill Climbing")
    # Get a fully solved state for a given n
    start = time.time()
    solution = nq.n_queens(n, choice = 1)
    end = time.time()
    print_solution(solution, n, "Hill Climbing", end - start, 1)
    print("Hill Climbing takes {} seconds to run".format(end - start))
    print("----------------------------------------------------------------")
    print("Using Simulated Annealing")
    start = time.time()
    solution = nq.n_queens(n, choice = 2, t = 30.0, cr = 0.94, iter = 50, threshold = 1e-5)
    end = time.time()
    print_solution(solution, n, "Simulated Annealing", end - start, 2)
    print("Simulated Annealing takes {} seconds to run".format(end - start))
    plt.show()

def experiment(n_start, n_end, method = "Hill", **kwargs):
    choice = None
    t = None
    cr = None
    iter = None
    threshold = None
    name = None
    if method == "Hill":
        choice = 1
        name = "Hill Climbing"
    elif method == "Sim":
        choice = 2
        t = float(kwargs["t"])
        cr = float(kwargs["cr"])
        iter = int(kwargs["iter"])
        threshold = float(kwargs["threshold"])
        name = "Simulated Annealing"
    else:
        print("Invalid Method Selection")
        return

    result = []
    total_time = []
    another_one = []
    for n in range(n_start, n_end):
        another_one.append([n])
        for i in range(20):
            start = time.time()
            solution = nq.n_queens(n, choice=choice, t = t, cr = cr, iter = iter, threshold = threshold)
            end = time.time()
            used_time = end - start
            total_time.append(used_time)
            result.append([n, 1000 * used_time])
            another_one[n-6].append(1000 * used_time)
        print("n = {} {} takes average {} millisecond to run for 20 times".format(n, name, 1000 * sum(total_time) / 20))

        total_time.clear()

    x = []
    y = []
    y_error = []
    current_tag = None
    temp = []
    for i, record in enumerate(result):
        n, time_record = record
        if current_tag == None:
            current_tag = n
            x.append(n)

        if n == current_tag:
            temp.append(time_record)
            if i == len(result) - 1:
                y.append(statistics.mean(temp))
                y_error.append(statistics.stdev(temp))
                temp.clear()


        elif n != current_tag:
            x.append(n)
            current_tag = n
            y.append(statistics.mean(temp))
            y_error.append(statistics.stdev(temp))
            temp.clear()


    plt.figure()
    plt.errorbar(x, y, xerr=0, yerr=y_error, fmt="o", ls='none')
    plt.xticks((np.arange(min(x), max(x)+1, 1.0)))
    plt.title("Execution Time of {} VS n".format(name))
    plt.show()

    df = pd.DataFrame(np.asarray(another_one))
    df.to_excel("{} result n from {} to {}.xlsx".format(name, n_start, n_end))

if __name__ == "__main__":
    # Parameters
    n = 6 # Control the board size that is used for direct compareson between the two algorithms
    n_start = 6 # Control the starting size of the chess board for the experiment
    n_end = 8 # Control the ending size of the chess board for the experiment

    # Run Simulated Annealing and Hill Climbing on n-queen problem, and plot solutions found by two methods
    direct_compare(n)
    # Run Hill Climbing for n ranging from n_start to n_end and plot error bar graph, and save result to excel at current directory
    experiment(n_start, n_end, "Hill")
    # Run Simulated Annealing for n ranging from n_start to n_end and plot error bar graph, and save result to excel at current directory
    # You can fine tune the Parameters that is passed into Simulated Annealing
    # t = temperature, cr = cooling rate, iter = the number of iteration per temperature drop, threshold = threshold
    experiment(n_start, n_end, "Sim", t = 30.0, cr = 0.98, iter = 30, threshold = 0.1)
