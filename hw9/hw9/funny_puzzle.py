import heapq
import numpy as np
import copy


def get_manhattan_distance(from_state, to_state=[1, 2, 3, 4, 5, 6, 7, 0, 0]):
    """
    TODO: implement this function. This function will not be tested directly by the grader. 

    INPUT: 
        Two states (if second state is omitted then it is assumed that it is the goal state)

    RETURNS:
        A scalar that is the sum of Manhattan distances for all tiles.
    """
    distance = 0
    coordinates = {1: (0,0), 2: (0, 1), 3: (0, 2), 4: (1, 0), 5: (1, 1), 6: (1, 2),
                    7: (2, 0)}
    for i in range(9):
        tile_val = from_state[i]
        if(tile_val != 0):
            g_row, g_col = coordinates[tile_val]
            #print(g_row)
            #print(g_col)
            c_row = (int)(i / 3)
            c_col = i % 3
            #print(c_row)
            #print(c_col)
            distance += abs(g_row - c_row) + abs(g_col - c_col)
    return distance




def print_succ(state):
    """
    TODO: This is based on get_succ function below, so should implement that function.

    INPUT: 
        A state (list of length 9)

    WHAT IT DOES:
        Prints the list of all the valid successors in the puzzle. 
    """
    succ_states = get_succ(state)

    for succ_state in succ_states:
        print(succ_state, "h={}".format(get_manhattan_distance(succ_state)))


def get_succ(state):
    """
    TODO: implement this function.

    INPUT: 
        A state (list of length 9)

    RETURNS:
        A list of all the valid successors in the puzzle (don't forget to sort the result as done below). 
    """
    succ_states = []
    succs = state
    npsuccs = np.array(succs)
    npsuccs2d = np.reshape(npsuccs,(3, 3))
    #npsuccs1d = np.reshape(npsuccs2d,(-1))
    # up
    for i in range(3):
        for j in range(3):
            if(npsuccs2d[i][j] == 0):
                # up 
                if(i - 1 >= 0 and npsuccs2d[i-1][j] != 0):
                    # append 
                    candidate = copy.deepcopy(npsuccs2d)
                    candidate[i][j], candidate[i-1][j] = candidate[i-1][j], candidate[i][j]
                    succ_states.append(np.reshape(candidate,(-1)).tolist())
                # down
                if(i + 1 <= 2 and npsuccs2d[i+1][j] != 0):
                    # append
                    candidate = copy.deepcopy(npsuccs2d)
                    candidate[i][j], candidate[i+1][j] = candidate[i+1][j], candidate[i][j]
                    succ_states.append(np.reshape(candidate,(-1)).tolist())
                # left
                if(j - 1 >= 0 and npsuccs2d[i][j-1] != 0):
                    # append
                    candidate = copy.deepcopy(npsuccs2d)
                    candidate[i][j], candidate[i][j-1] = candidate[i][j-1], candidate[i][j]
                    succ_states.append(np.reshape(candidate,(-1)).tolist())
                # right
                if(j + 1 <= 2 and npsuccs2d[i][j+1] != 0):
                    # append
                    candidate = copy.deepcopy(npsuccs2d)
                    candidate[i][j], candidate[i][j+1] = candidate[i][j+1], candidate[i][j]
                    succ_states.append(np.reshape(candidate,(-1)).tolist())
    return sorted(succ_states)

def get_path(path, start, end):
    reverse_path = [end]
    while(end != start):
        end = path[str(end)]
        reverse_path.append(end)
    return list(reversed(reverse_path))

# def print_path(reversed_list):
#     for state in reversed_list:
#         print(state, "h={}".format(get_manhattan_distance(state)), 
#         "moves: {}".format)

def solve(state, goal_state=[1, 2, 3, 4, 5, 6, 7, 0, 0]):
    """
    TODO: Implement the A* algorithm here.

    INPUT: 
        An initial state (list of length 9)

    WHAT IT SHOULD DO:
        Prints a path of configurations from initial state to goal state along  h values, number of moves, and max queue number in the format specified in the pdf.
    """
    visited = set()
    path = dict()
    distance = {str(state): 0}
    max_queue_length = -1
    OPEN = []
    cost = 0
    g = 0
    h = get_manhattan_distance(state, goal_state)
    p_index = -1
    heapq.heappush(OPEN, (cost, state, (g, h, p_index)))
    while OPEN:
        if(max_queue_length < len(OPEN)):
            max_queue_length = len(OPEN)
        node = heapq.heappop(OPEN)
        if str(node[1]) in visited:
            continue
        if node[1] == goal_state:
            reversed_path = get_path(path, state, goal_state)
            for state in reversed_path:
                print(state, "h={}".format(get_manhattan_distance(state)),
                "moves: {}".format(distance[str(state)]))
            print("Max queue length: {}".format(max_queue_length))
            break
        visited.add(str(node[1]))
        for succ in get_succ(node[1]):
            g = node[2][0] + 1
            h = get_manhattan_distance(succ, goal_state)
            p_index = node[2][2] + 1
            cost = g + h
            heapq.heappush(OPEN, (cost, succ, (g, h, p_index)))
            if(str(succ) not in distance
                or distance[str(node[1])] + 1 < distance[str(succ)]):
                distance[str(succ)] = distance[str(node[1])] + 1
                path[str(succ)] = node[1]

if __name__ == "__main__":
    """
    Feel free to write your own test code here to exaime the correctness of your functions. 
    Note that this part will not be graded.
    """
    #print_succ([2,5,1,4,0,6,7,0,3])
    #print()

    #print(get_manhattan_distance([2,5,1,0,4,6,7,0,3], [1, 2, 3, 4, 5, 6, 7, 0, 0]))
    #print()

    #solve([4, 3, 0, 5, 1, 6, 7, 2, 0])
    #print()
    
