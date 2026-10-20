
"""
AINL3001 — Knowledge-Driven AI
Week 6 — Adversarial Search (Tic-Tac-Toe)
BSP 2026

X is MAX (+1 for a win); O is MIN (-1 for a win).
A draw has utility 0. Search assumes both players play optimally.

Tasks:
0. Evaluate a small game tree manually.
1. Represent and display a board; implement legal moves.
2. Check winners, terminal states and utility.
3. Implement Minimax.
4. Choose the best move for X.
5. Count visited game-tree nodes.
6. Implement Alpha-Beta Pruning and compare results.

Extensions: depth-limited search, heuristic evaluation, Connect Four.
"""

# TASK 0 — MANUAL MINIMAX
print("=" * 50)
print("TASK 0 — MANUAL MINIMAX")
print("=" * 50)
print(r"""
            MAX
           /   \
         MIN   MIN
        /  \   /  \
       3    5  2    9
""")
print("Which values do the two MIN nodes return?")
print("Which branch should MAX choose, and why?")

# BOARD — X plays next (three X marks and two O marks).
# Board positions are numbered 0 to 8, left to right, top to bottom.
board = [
    "X", "O", "X",
    " ", "O", " ",
    " ", " ", "X",
]

WINNING_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
]

"""
TASK 0 ANSWERS

Left MIN = min(3, 5) = 3
Right MIN = min(2, 9) = 2

MAX chooses the left branch because 3 > 2.

MIN picks the smallest value because it wants
the worst outcome for MAX.

MAX picks the largest value because it wants
the best possible outcome.
"""

# --------------------------------------------------
# TASK 1 — BOARD REPRESENTATION
# --------------------------------------------------

def print_board(state):
    """Display the nine cells as a 3-by-3 board."""
    # TODO: Print three rows of three cells.
    for i in range(0, 9, 3):  # print 3 cells at a time
        print(" | ".join(state[i:i + 3]))  # display one row

        if i < 6:  # add a separator after the first two rows
            print("---+---+---")


# --------------------------------------------------
# TASK 1 — AVAILABLE MOVES
# --------------------------------------------------

def available_moves(state):
    """Return indices of empty cells (0 through 8)."""
    # TODO: Find every position containing " ".
    return [i for i in range(9) if state[i] == " "]  # empty cells


# --------------------------------------------------
# TASK 1 — MAKE A MOVE
# --------------------------------------------------

def make_move(state, move, player):
    """Return a NEW board with player ('X' or 'O') at move.

    Assume move is legal. Do not modify the input board.
    """
    # TODO: Copy the board and place the player's mark.
    new_state = state.copy()  # don't change the original
    new_state[move] = player  # put X or O into the cell
    return new_state  # return the copied board


# --------------------------------------------------
# TASK 2 — WINNER
# --------------------------------------------------

def check_winner(state):
    """Return 'X', 'O' or None by checking all winning lines."""
    # TODO: Check each (a, b, c) in WINNING_LINES.
    for a, b, c in WINNING_LINES:  # check every winning line

        if state[a] != " " and state[a] == state[b] == state[c]:
            return state[a]  # return X or O

    return None  # no winner found


# --------------------------------------------------
# TASK 2 — TERMINAL STATE
# --------------------------------------------------

def is_terminal(state):
    """Return True for a win or a full board (draw)."""
    # TODO: Detect a winner OR no remaining empty cells.
    return check_winner(state) is not None or " " not in state  # win or draw


# --------------------------------------------------
# TASK 2 — UTILITY
# --------------------------------------------------

def utility(state):
    """Return +1 for X win, -1 for O win, 0 for draw/no winner.

    Minimax calls this only at terminal states.
    """
    # TODO: Use check_winner() and return +1, -1 or 0.
    winner = check_winner(state)  # see who won

    if winner == "X":  # X wins
        return 1

    if winner == "O":  # O wins
        return -1

    return 0  # draw or no winner


# --------------------------------------------------
# TASK 3 — MINIMAX
# --------------------------------------------------

def minimax(state, maximizing, counter):
    """Return game-theoretic score; count every visited node.

    maximizing=True means X moves next; False means O moves next.
    counter is a one-item dictionary: {'nodes': 0}.
    """
    # TODO:
    # 1. Count this node: counter["nodes"] += 1.
    # 2. If terminal, return utility(state).
    # 3. For X (MAX), recursively choose the highest score.
    # 4. For O (MIN), recursively choose the lowest score.
    # Use make_move() to avoid changing the original board.

    counter["nodes"] += 1  # count every visited node

    if is_terminal(state):  # stop when the game ends
        return utility(state)  # score the result

    if maximizing:  # X wants the highest score
        best = -float("inf")  # start very low

        for move in available_moves(state):  # try every X move
            next_state = make_move(state, move, "X")  # copy and play X
            score = minimax(next_state, False, counter)  # O goes next
            best = max(best, score)  # keep largest score

        return best

    else:  # O wants the lowest score
        best = float("inf")  # start very high

        for move in available_moves(state):  # try every O move
            next_state = make_move(state, move, "O")  # copy and play O
            score = minimax(next_state, True, counter)  # X goes next
            best = min(best, score)  # keep smallest score

        return best


# --------------------------------------------------
# TASK 4 AND 5 — BEST MOVE
# --------------------------------------------------

def best_move(state, counter):
    """Return the best move index for X, or None if game is over.

    Count nodes in recursive Minimax searches. Ties use first move.
    """
    # TODO: Try each legal X move, call minimax() for O's turn,
    # and return the move with the highest score.
    # If the board is terminal, return None.

    if is_terminal(state):  # game already ended
        return None

    best_score = -float("inf")  # lowest starting score
    chosen_move = None  # no move selected yet

    for move in available_moves(state):  # try each legal move
        next_state = make_move(state, move, "X")  # X makes this move
        score = minimax(next_state, False, counter)  # O plays next

        if score > best_score:  # first move wins any tie
            best_score = score  # save better score
            chosen_move = move  # save its position

    return chosen_move  # best move for X


# --------------------------------------------------
# TASK 6 — ALPHA-BETA PRUNING
# --------------------------------------------------

def alpha_beta(state, maximizing, alpha, beta, counter):
    """Return the same score as Minimax, pruning irrelevant branches.

    alpha = best score MAX can guarantee so far.
    beta  = best score MIN can guarantee so far.
    """
    # TODO: Adapt minimax():
    # - MAX updates alpha; MIN updates beta.
    # - Stop exploring remaining moves if alpha >= beta.
    # - Count visited nodes exactly as in minimax().

    counter["nodes"] += 1  # count this node, including terminal nodes

    if is_terminal(state):  # game finished
        return utility(state)  # return its score

    if maximizing:  # X wants the highest score
        best = -float("inf")

        for move in available_moves(state):  # check X moves
            next_state = make_move(state, move, "X")  # X goes here
            score = alpha_beta(next_state, False, alpha, beta, counter)  # O next

            best = max(best, score)  # keep best X score
            alpha = max(alpha, best)  # update MAX's bound

            if alpha >= beta:  # remaining branches cannot help
                break  # skip them

        return best

    else:  # O wants the lowest score
        best = float("inf")

        for move in available_moves(state):  # check O moves
            next_state = make_move(state, move, "O")  # O goes here
            score = alpha_beta(next_state, True, alpha, beta, counter)  # X next

            best = min(best, score)  # keep best O score
            beta = min(beta, best)  # update MIN's bound

            if alpha >= beta:  # remaining branches cannot help
                break  # skip them

        return best


# --------------------------------------------------
# TASK 6 — BEST MOVE WITH ALPHA-BETA
# --------------------------------------------------

def best_move_alpha_beta(state, counter):
    """Return the best move index for X using Alpha-Beta search."""
    # TODO: Like best_move(), but call alpha_beta().
    # Start alpha at -infinity and beta at +infinity.
    # Update alpha after each candidate X move.

    if is_terminal(state):  # game already over
        return None

    best_score = -float("inf")  # lowest starting score
    chosen_move = None  # no move chosen
    alpha = -float("inf")  # MAX's current lower bound
    beta = float("inf")  # MIN's current upper bound

    for move in available_moves(state):  # try each X move
        next_state = make_move(state, move, "X")  # make a copy and play X
        score = alpha_beta(next_state, False, alpha, beta, counter)  # O next

        if score > best_score:  # prefer first move on ties
            best_score = score  # keep highest score
            chosen_move = move  # remember that move

        alpha = max(alpha, best_score)  # update alpha for next move

    return chosen_move  # best move for X


# --------------------------------------------------
# TESTING — RUN PYTHON FILE IN VS CODE
# --------------------------------------------------

if __name__ == "__main__":
    print("\nCurrent board (X to move):")
    print_board(board)
    print("\nAvailable moves:", available_moves(board))
    print("Winner:", check_winner(board))
    print("Terminal:", is_terminal(board))
    print("Utility:", utility(board))

    # For a meaningful comparison, both algorithms use the same board
    # and count the same thing: recursive game-tree nodes visited.
    minimax_counter = {"nodes": 0}
    move_minimax = best_move(board, minimax_counter)
    print("\nMinimax best move for X:", move_minimax)
    print("Minimax nodes visited:", minimax_counter["nodes"])

    # TASK 5 ANSWERS
    # Minimax visits 31 nodes from the supplied starting board.
    # Every recursive call counts, including terminal states.
    # We count game-tree nodes, not unique board positions.
    # Larger games have many more possible moves to explore.

    alpha_beta_counter = {"nodes": 0}
    move_ab = best_move_alpha_beta(board, alpha_beta_counter)
    print("\nAlpha-Beta best move for X:", move_ab)
    print("Alpha-Beta nodes visited:", alpha_beta_counter["nodes"])

    if move_minimax is not None:
        print("\nBoard after Minimax move:")
        print_board(make_move(board, move_minimax, "X"))

    print("\nReflection:")
    print("1. Why is Tic-Tac-Toe a search problem?")
    print("2. Why does Minimax assume an optimal opponent?")
    print("3. What is the purpose of a utility function?")
    print("4. What happens as games become larger?")


"""
REFLECTION ANSWERS

1. Why is Tic-Tac-Toe considered a search problem?
Because the AI searches possible moves and future boards to find the best move.

2. Why does Minimax assume an optimal opponent?
Because it prepares for the opponent choosing the best possible move.

3. What is the purpose of a utility function?
It measures the final outcome of a game:
X win = +1, O win = -1, draw = 0.

4. What happens as games become larger?
There are more possible moves and states, so searching becomes slower.
"""
