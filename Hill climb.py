import random

# Generate a random board of size N
def random_board(N):
    # one queen per column, random row for each column
    return [random.randint(0, N - 1) for _ in range(N)]

# Calculate heuristic: number of attacking pairs
def heuristic(state):
    h = 0
    N = len(state)
    for i in range(N):
        for j in range(i + 1, N):
            # same row or same diagonal means attack
            if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                h += 1
    return h

# Generate all possible moves (neighbors)
def all_possible_moves(state):
    N = len(state)
    neighbors = []
    for col in range(N):
        for row in range(N):
            if row != state[col]:  # move queen to a different row
                new_state = state.copy()
                new_state[col] = row
                neighbors.append(new_state)
    return neighbors

# Return the neighbor with the lowest heuristic
def state_with_lowest_h(neighbors):
    best_state = neighbors[0]
    best_h = heuristic(best_state)
    for s in neighbors[1:]:
        h = heuristic(s)
        if h < best_h:
            best_h = h
            best_state = s
    return best_state, best_h

# Hill climbing with random restarts
def hill_climbing(N):
    attempts = 0
    while True:
        attempts += 1
        state = random_board(N)
        h = heuristic(state)

        while True:
            if h == 0:
                print(f"✅ Solution found after {attempts} attempts!")
                return state

            neighbors = all_possible_moves(state)
            next_state, next_h = state_with_lowest_h(neighbors)

            # If no improvement → stuck in local minimum
            if next_h >= h:
                break

            # Move to better neighbor
            state, h = next_state, next_h

# -------------------------------
# Run for N = 4
# -------------------------------
solution = hill_climbing(4)
print("Final board state:", solution)
print("Heuristic value:", heuristic(solution))
