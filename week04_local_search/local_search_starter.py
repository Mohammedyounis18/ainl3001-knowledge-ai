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


"""
TASK 4 / HILL CLIMBING QUESTIONS

Does Hill Climbing always find a solution?
No.

Can it stop with conflicts remaining?
Yes.

Why can it stop before reaching 0 conflicts?
Because it only accepts a better neighbour.
If no nearby board has a lower cost, it stops.

What is a local minimum?
A board that is better than all of its neighbours,
but still has conflicts.

What is a plateau?
A group of nearby boards with the same cost.
"""


# --------------------------------------------------
# TASK 4 — SIMULATED ANNEALING
# --------------------------------------------------

def simulated_annealing(problem, start_board):
    """
    Use Simulated Annealing to search for
    a solution.

    Unlike Hill Climbing, Simulated Annealing
    can sometimes accept a worse state.

    This can help escape local minima.
    """

    current = start_board  # begin with the starting board

    temperature = 10.0  # high temperature means more exploration
    cooling_rate = 0.95  # slowly reduce the temperature

    # TODO

    while temperature > 0.01:  # stop when the system becomes very cold

        current_cost = count_conflicts(current)  # cost of current board

        if current_cost == 0:  # stop early if we find a solution
            return current

        neighbours = generate_neighbours(problem, current)  # get possible next boards

        next_board = random.choice(neighbours)  # randomly choose one neighbour

        next_cost = count_conflicts(next_board)  # cost of that neighbour

        difference = next_cost - current_cost  # negative means the new board is better

        if difference < 0:  # always accept a better board
            current = next_board

        else:
            probability = math.exp(-difference / temperature)  # chance of accepting worse move

            if random.random() < probability:  # randomly decide whether to accept it
                current = next_board

        temperature *= cooling_rate  # make worse moves less likely over time

    return current  # return the best place this run ended


"""
SIMULATED ANNEALING QUESTIONS

1. Why might accepting a worse move be useful?
   It can help the algorithm escape a local minimum.

2. What happens when the temperature is high?
   Worse moves are more likely to be accepted,
   so the algorithm explores more.

3. What happens as the temperature decreases?
   Worse moves become less likely.
   The algorithm becomes more selective.
"""


# --------------------------------------------------
# TESTING AREA
# --------------------------------------------------

if __name__ == "__main__":

    board = [
        random.randint(0, N - 1)
        for _ in range(N)
    ]

    problem = QueensProblem(board)

    print("\nRandom Board")
    print(board)

    print("\nConflicts")
    print(
        count_conflicts(board)
    )

    print("\nPossible Actions")

    actions = problem.actions(board)

    print(
        f"{len(actions)} actions available"
    )

    print("\nNeighbours")

    neighbours = generate_neighbours(
        problem,
        board
    )

    print(
        f"{len(neighbours)} neighbours generated"
    )

    print("\nHill Climbing - 5 Attempts")

    hill_best = None  # store the lowest Hill Climbing cost found

    for attempt in range(1, 6):  # run Hill Climbing 5 times

        start_board = [
            random.randint(0, N - 1)
            for _ in range(N)
        ]  # make a new random starting board

        attempt_problem = QueensProblem(start_board)  # create the problem

        final_board = hill_climbing(
            attempt_problem,
            start_board
        )  # run Hill Climbing

        final_cost = count_conflicts(final_board)  # measure the result

        print(
            f"Attempt {attempt}: cost = {final_cost}, board = {final_board}"
        )

        if hill_best is None or final_cost < hill_best:  # keep the best result
            hill_best = final_cost

    print("\nSimulated Annealing - 5 Attempts")

    annealing_best = None  # store the lowest Simulated Annealing cost found

    for attempt in range(1, 6):  # run Simulated Annealing 5 times

        start_board = [
            random.randint(0, N - 1)
            for _ in range(N)
        ]  # make a new random starting board

        attempt_problem = QueensProblem(start_board)  # create the problem

        final_board = simulated_annealing(
            attempt_problem,
            start_board
        )  # run Simulated Annealing

        final_cost = count_conflicts(final_board)  # measure the result

        print(
            f"Attempt {attempt}: cost = {final_cost}, board = {final_board}"
        )

        if annealing_best is None or final_cost < annealing_best:  # keep the best result
            annealing_best = final_cost

    print("\nBest Costs")
    print("Hill Climbing:", hill_best)
    print("Simulated Annealing:", annealing_best)


# --------------------------------------------------
# ALGORITHM COMPARISON ANSWERS
# --------------------------------------------------

"""
Do both algorithms always produce the same result?
No. They can finish on different boards.

Which algorithm shows more variation?
Simulated Annealing, because randomness affects its moves.

How do occasional worse moves affect the search?
They let Simulated Annealing escape places where Hill Climbing
could get stuck.

What trade-off does Simulated Annealing introduce?
It can explore more and escape local minima,
but its result is less predictable and it may take more work.
"""


# --------------------------------------------------
# REFLECTION QUESTIONS
# --------------------------------------------------

"""
1. What is the difference between search and optimisation?

Search usually tries to find a path to a goal.
Optimisation tries to improve a candidate solution.


2. Why does an optimisation problem need a way to evaluate
   candidate solutions?

So the algorithm can tell which solution is better.
Here we use the number of queen conflicts.


3. Why can Hill Climbing become stuck in a local minimum?

Because it only moves to a better neighbour.
If every nearby state is the same or worse, it stops.


4. What is a plateau?

A group of nearby states that all have the same cost.


5. How does Simulated Annealing overcome some limitations
   of Hill Climbing?

It sometimes accepts worse moves.
This can help it escape a local minimum or plateau.


6. What is the difference between deterministic and stochastic search?

Deterministic behaviour follows the same decision rule
and makes the same choice from the same situation.

Stochastic behaviour uses randomness,
so different runs can make different choices.


7. How did the Problem representation allow us to represent
   both a grid world and N-Queens?

Both problems use the same ideas:
initial state, actions, and result.

The actual states and actions can still be completely different.


8. How do optimisation techniques relate to Machine Learning?

Machine Learning also tries to improve a solution
by reducing a cost or error.

For example, training a model tries to reduce its loss.
"""
