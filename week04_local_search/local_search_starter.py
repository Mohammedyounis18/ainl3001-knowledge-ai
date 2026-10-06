"""
AINL3001 — Knowledge-Driven AI
Week 4 — Local Search and Optimisation
BSP 2026

This week introduces local search.

In previous weeks, search algorithms explored paths through
a state space in order to reach a goal.

Local search takes a different approach:

    1. Start with a state.
    2. Evaluate how good that state is.
    3. Generate neighbouring states.
    4. Move to a better neighbour.
    5. Repeat.

We will explore this using the N-Queens problem.

Tasks
-----

1. Understand the problem representation.
2. Implement conflict counting.
3. Explore neighbouring states.
4. Implement Hill Climbing.
5. Implement Simulated Annealing.
"""

import math
import random

from queens_problem import QueensProblem

N = 8


# --------------------------------------------------
# TASK 0 — UNDERSTANDING THE STATE
# --------------------------------------------------

example_board = [0, 1, 2, 3]

print("Manual Exploration Board:")
print(example_board)

print(
    "\nEach list position represents a column."
)

print(
    "Each value represents the row containing the queen."
)

print(
    "\nQuestion: How many conflicts exist on this board?"
)

"""
TASK 0 ANSWERS

1. How many pairs of queens are attacking each other?
   6 pairs.

   All four queens are on the same diagonal.
   With 4 queens there are 6 different pairs.

2. Is it a valid solution?
   No, because the queens attack each other.

3. Could moving one queen reduce the conflicts?
   Yes. Moving a queen away from the diagonal can reduce conflicts.

Discussion:
Why measure the quality of a candidate solution?
So the AI can compare boards and know which board is better.
Here, fewer conflicts means a better board.
"""


# --------------------------------------------------
# TASK 1 — EVALUATE A STATE
# --------------------------------------------------

def count_conflicts(board):
    """
    Return the number of pairs of queens
    that attack each other.

    Lower values are better.

    A solution has:

        conflict count = 0
    """

    # TODO:
    # Compare each queen with every queen
    # that comes after it.
    #
    # Queens conflict when they are:
    #
    #   1. in the same row
    #   2. on the same diagonal

    conflicts = 0  # start with no conflicts

    for col1 in range(len(board)):  # choose the first queen
        for col2 in range(col1 + 1, len(board)):  # compare only with queens after it

            row1 = board[col1]  # row of the first queen
            row2 = board[col2]  # row of the second queen

            same_row = row1 == row2  # true if both queens are in the same row

            same_diagonal = abs(row1 - row2) == abs(col1 - col2)  # same diagonal check

            if same_row or same_diagonal:  # if they can attack each other
                conflicts += 1  # count this pair once

    return conflicts  # lower is better, 0 is a solution


# --------------------------------------------------
# TASK 2 — EXPLORE THE PROBLEM
# --------------------------------------------------

def generate_neighbours(problem, board):
    """
    Generate all neighbouring boards.

    Use the Problem interface introduced this week:

        problem.actions(state)
        problem.result(state, action)
    """

    neighbours = []

    # TODO:
    #
    # 1. Ask the problem for the available actions.
    # 2. Apply each action.
    # 3. Add the resulting state to neighbours.

    actions = problem.actions(board)  # get every valid queen move

    for action in actions:  # go through each possible move
        neighbour = problem.result(board, action)  # make that move
        neighbours.append(neighbour)  # save the new board

    return neighbours


"""
TASK 2 QUESTIONS

1. How many alternative rows can each queen move to?
   7 rows.

2. How many neighbours should an 8x8 board generate?
   8 queens x 7 alternative rows = 56 neighbours.

3. Why can generating every neighbour become expensive?
   Bigger boards create many more possible moves,
   so the computer has more states to generate and check.
"""

# --------------------------------------------------
# TASK 3 — HILL CLIMBING
# --------------------------------------------------

def hill_climbing(problem, start_board):
    """
    Use Hill Climbing to reduce the number
    of conflicts.

    Algorithm:

        current = start state

        repeat:

            generate neighbours

            find the neighbour with the
            lowest conflict count

            if the neighbour is not better:
                stop

            otherwise:
                move to the neighbour

        return current
    """

    current = start_board  # begin with the starting board

    # TODO

    while True:  # keep improving until no better neighbour exists

        current_cost = count_conflicts(current)  # cost of the current board

        if current_cost == 0:  # 0 conflicts means we found a solution
            return current

        neighbours = generate_neighbours(problem, current)  # generate nearby boards

        best_neighbour = min(neighbours, key=count_conflicts)  # board with lowest cost

        best_cost = count_conflicts(best_neighbour)  # cost of the best neighbour

        if best_cost >= current_cost:  # if no neighbour is better
            return current  # stop at the current board

        current = best_neighbour  # move to the better board

