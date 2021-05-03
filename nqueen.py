import random
import copy
import math

def get_random_state(n):
    state = []
    # Your code here
    candidates = [0]*n
    for i in range(1, n+1):
        candidates[i-1] = i
    for i in range(0, n):
        choice = random.choice(candidates)
        candidates.remove(choice)
        state.append(choice)
    return state

'''
Compute pairs of queens in conflict
'''
def getPermutation(size):
    return size*(size-1)//2

def compute_attacking_pairs(state):
    number_attacking_pairs = 0
    # Your code here
    n = len(state)
    row_count = [0]*n
    primatry_diag_count = [0]*(2*n-1)
    secondary_diag_count = [0]*(2*n-1)
    #     c0  c1  c2  c3
    # r0 |___|___|___|___|
    # r1 |___|___|___|___|
    # r2 |___|___|___|___|
    # r3 |___|___|___|___|
    for i in range(0, n):
        row_count[state[i]-1] += 1
        secondary_diag_count[state[i] - 1 + i] += 1
        primatry_diag_count[n - state[i] + i] += 1
    for i in range(0, 2*n-1):
        if i < n:
            frequency = row_count[i]
            number_attacking_pairs += getPermutation(frequency)
        number_attacking_pairs += getPermutation(primatry_diag_count[i])
        number_attacking_pairs += getPermutation(secondary_diag_count[i])

    return number_attacking_pairs

'''
The basic hill-climing algorithm for n queens
'''
def hill_desending_n_queens(state, comp_att_pairs):
    final_state = []
    # Your code here
    current_best_value = comp_att_pairs(state)
    next_best_value = current_best_value
    n = len(state)
    final_state = state.copy()
    while True:

        for i in range (0, n):
            test_bord = final_state.copy()
            neighbors = get_neighbors(test_bord, i, n)
            for neighbor in neighbors:
                test_bord[i] = neighbor
                num_pair = comp_att_pairs(test_bord)
                if num_pair == 0:
                    return test_bord
                elif next_best_value > num_pair:
                    final_state = test_bord.copy()
                    next_best_value = num_pair

        if next_best_value < current_best_value:
            current_best_value = next_best_value
        else:
            break

    return final_state

def get_neighbors(state, i, n):
    result = []
    for j in range(1, n+1):
        if state[i] == j:
            continue
        result.append(j)
    return result

def generate_neighbor(state, n):
    #Method 1
    row1 = random.randint(0, n-1)
    row2 = random.randint(0, n-1)
    if row2 == row1:
        if row2 == n-1:
            row2 -= 1
        elif row2 == 0:
            row2 += 1
        else:
            row2 += 1
    assert row2 != row1
    result = copy.deepcopy(state)
    result[row1], result[row2] = result[row2], result[row1]
    
    # Method 2

    # row1 = random.randint(0, n-1)
    # position = random.randint(1, n)
    # current_position = state[row1]
    # if current_position == position:
    #     if current_position == n:
    #         position-=1
    #     else:
    #         position+=1
    # result = copy.deepcopy(state)
    # result[row1] = position
    # assert result != state
    return result



'''
Hill-climing algorithm for n queens with restart
'''
def n_queens(n, **kwargs):
    final_state = []
    # Your code here
    choice = kwargs["choice"]
    if choice == 1:
        while True:
            final_state = get_random_state(n)
            final_state = hill_desending_n_queens(final_state, compute_attacking_pairs)
            if compute_attacking_pairs(final_state) == 0:
                break
        return final_state
    elif choice == 2:
        temperature = float(kwargs["t"])
        cooling_rate = float(kwargs["cr"])
        iteration = int(kwargs["iter"])
        threshold = float(kwargs["threshold"])
        initial_state = get_random_state(n)
        heuristic = compute_attacking_pairs(initial_state)

        while temperature > threshold or heuristic != 0:
            for i in range(iteration):
                neighbor = generate_neighbor(initial_state, n)
                new_heuristic = compute_attacking_pairs(neighbor)
                if new_heuristic == 0:
                    return neighbor
                elif new_heuristic < heuristic:
                    initial_state = copy.deepcopy(neighbor)
                    heuristic = new_heuristic
                else:
                    delta = new_heuristic - heuristic
                    probability = math.exp(-delta/temperature)
                    rand = random.uniform(0, 1)
                    if rand < probability:
                        initial_state = copy.deepcopy(neighbor)
                        heuristic = new_heuristic
            temperature *= cooling_rate

        if heuristic == 0:
            return initial_state
        else:
            return []
