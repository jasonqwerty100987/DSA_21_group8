import nqueen as nq
import time as t
import pprint
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
    # pprint.pprint(result)

if __name__ == "__main__":

    n = int(sys.argv[1])
    print("n = {}".format(n))
    # print(nq.get_random_state(n))
    # print("Using Hill Climbing")
    # # Get a fully solved state for a given n
    # start = t.time()
    # solution = nq.n_queens(n, choice = 1)
    # end = t.time()
    # print("A valid solution: ")
    # print_solution(solution, n, "Hill Climbing", end - start, 1)
    # print("Hill Climbing takes {} seconds to run".format(end - start))
    # print("----------------------------------------------------------------")
    # print("Using Simulated Annealing")
    # start = t.time()
    # solution = nq.n_queens(n, choice = 2, t = 30.0, cr = 0.94, iter = 50, threshold = 1e-5)
    # end = t.time()
    # print("A valid solution: ")
    # print_solution(solution, n, "Simulated Annealing", end - start, 2)
    # print("Simulated Annealing takes {} seconds to run".format(end - start))
    # plt.show()
    result = []
    total_time = []
    another_one = []
    for n in range(6, 30):
        another_one.append([n])
        for i in range(20):
            start = t.time()
            solution = nq.n_queens(n, choice=1, t = 30.0, cr = 0.94, iter = 50, threshold = 1e-5)
            end = t.time()
            used_time = end - start
            total_time.append(used_time)
            result.append([n, 1000 * used_time])
            another_one[n-6].append(1000 * used_time)
        # print("A valid solution: ")
        # print_solution(solution, n)
        # print("Hill Climbing takes {} seconds to run".format(end - start))
        print("n = {} Simulated Annealing takes average {} millisecond to run for 20 times".format(n, 1000 * sum(total_time) / 20))

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
    plt.title("Execution Time of Hill Climbing VS n")
    plt.show()



    df = pd.DataFrame(np.asarray(result), columns = ['n', 'Execution of in millisecond'])
    df.to_excel("Hill Climbing error bar.xlsx")

    df = pd.DataFrame(np.asarray(another_one))
    df.to_excel("Hill Climbing error bar1.xlsx")
