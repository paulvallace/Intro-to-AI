import heapq

def get_manhattan_distance(from_state, to_state=[1, 2, 3, 4, 5, 6, 7, 0, 0]):
    distance = 0
    for num in range(1, 8):  # Only calculate for tiles 1 to 7, not including 0's
        from_index = from_state.index(num)
        to_index = to_state.index(num)
        # Chatgpt gave me the function divmod 
        from_row, from_col = divmod(from_index, 3)
        to_row, to_col = divmod(to_index, 3)
        distance += abs(from_row - to_row) + abs(from_col - to_col)
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
    def swap(state, i, new_i):
        new_state= state[:]
        new_state[i], new_state[new_i] = new_state[new_i], new_state[i]
        return new_state

    succ_state = []
    for index, value in enumerate(state):
        if value == 0:
            if index == 0:
                succ_state.append(swap(state,index, index+1))
                succ_state.append(swap(state,index, index+3))
            if index ==1:
                succ_state.append(swap(state,index, index+1))
                succ_state.append(swap(state,index, index-1))
                succ_state.append(swap(state,index, index+3))
            if index==2:
                succ_state.append(swap(state,index, index-1))
                succ_state.append(swap(state,index, index+3))
            if index == 3:
                succ_state.append(swap(state,index, index+1))
                succ_state.append(swap(state,index, index+3))
                succ_state.append(swap(state,index, index-3))
            if index == 4:
                succ_state.append(swap(state,index, index+1))
                succ_state.append(swap(state,index, index-1))
                succ_state.append(swap(state,index, index-3))
                succ_state.append(swap(state,index, index+3))
            if index == 5:
                succ_state.append(swap(state,index, index-1))
                succ_state.append(swap(state,index, index+3))
                succ_state.append(swap(state,index, index-3))
            if index == 6:
                succ_state.append(swap(state,index, index+1))
                succ_state.append(swap(state,index, index-3))
            if index == 7:
                succ_state.append(swap(state,index, index+1))
                succ_state.append(swap(state,index, index-1))
                succ_state.append(swap(state,index, index-3))
            if index == 8:
                succ_state.append(swap(state,index, index-1))
                succ_state.append(swap(state,index, index-3))
            for success in succ_state:
                if success == state:
                    succ_state.remove(state)
    succ_state.sort()
    return succ_state

def solve(state, goal_state=[1, 2, 3, 4, 5, 6, 7, 0, 0]):
    """
    TODO: Implement the A* algorithm here.

    INPUT: 
        An initial state (list of length 9)

    WHAT IT SHOULD DO:
        Prints a path of configurations from initial state to goal state along  h values, number of moves, and max queue number in the format specified in the pdf.
    """

    # This is a format helper.
    # build "state_info_list", for each "state_info" in the list, it contains "current_state", "h" and "move".
    # define and compute max length
    # it can help to avoid any potential format issue.

    pq = []  # Priority queue
    heapq.heappush(pq, (0, state, 0, -1))  # (cost, state, move, parent)
    visited = set()  # Track visited states
    max_length = 0
    parent_map = {}  # To reconstruct the path
    state_info_list = []  # contains "current_state", "h" and "move".

    while pq:
        cost, current_state, moves, parent_index = heapq.heappop(pq)

        if tuple(current_state) in visited:
            continue

        visited.add(tuple(current_state))
        parent_map[tuple(current_state)] = parent_index

        if current_state == goal_state:
            # Reconstruct the path
            path = []
            while tuple(current_state) != tuple(state):
                path.append((current_state, get_manhattan_distance(current_state), moves))
                current_state = state_info_list[parent_map[tuple(current_state)]][0]
                moves -= 1
            path.append((state, get_manhattan_distance(state), 0))
            state_info_list = path[::-1]
            break

        for succ_state in get_succ(current_state):
            if tuple(succ_state) not in visited:
                new_moves = moves + 1
                h = get_manhattan_distance(succ_state)
                g = new_moves
                heapq.heappush(pq, (g + h, succ_state, new_moves, len(state_info_list)))

        state_info_list.append((current_state, get_manhattan_distance(current_state), moves))
        max_length = max(max_length, len(pq))  # Update max_length only after adding new states

    for state_info in state_info_list:
        current_state, h, move = state_info
        print(current_state, "h={}".format(h), "moves: {}".format(move))
    print("Max queue length: {}".format(max_length))


if __name__ == "__main__":
    """
    Feel free to write your own test code here to exaime the correctness of your functions. 
    Note that this part will not be graded.
    """
    print_succ([2,5,1,4,0,6,7,0,3])
    print()

    print(get_manhattan_distance([2,5,1,4,0,6,7,0,3], [1, 2, 3, 4, 5, 6, 7, 0, 0]))
    print()

    solve([2,5,1,4,0,6,7,0,3])
    print()
