"""
TU850-3
AINL3001 — Knowledge-Driven AI
Dr. Bianca Schoen-Phelan
2026

Week 4 Tutorial
Introducing the Problem Class

In previous weeks, we represented problems directly using
variables and functions.

From this week onwards, we will use a common Problem class
where appropriate.

This tutorial uses the familiar grid world from earlier weeks
to explore the new structure.
"""

from common.problem import Problem


GRID_SIZE = 5


class GridProblem(Problem):
    """
    A simple grid-world problem.

    A state is represented as an (x, y) coordinate.

    Example:

        (0, 0) = top-left corner
        (4, 4) = bottom-right corner
    """

    def actions(self, state):
        """
        Return the valid actions from this state.

        Possible actions:

            UP
            DOWN
            LEFT
            RIGHT

        Remember: an action must not move outside the grid.
        """

        # TODO:
        #
        # 1. Extract x and y from state.
        # 2. Create an empty list of actions.
        # 3. Check which movements are valid.
        # 4. Add valid actions to the list.
        # 5. Return the list.

        x, y = state  # get the x and y coordinates
        actions = []  # store the valid moves

        if y > 0:  # if we are not at the top edge
            actions.append("UP")  # allow UP

        if y < GRID_SIZE - 1:  # if we are not at the bottom edge
            actions.append("DOWN")  # allow DOWN

        if x > 0:  # if we are not at the left edge
            actions.append("LEFT")  # allow LEFT

        if x < GRID_SIZE - 1:  # if we are not at the right edge
            actions.append("RIGHT")  # allow RIGHT

        return actions  # return all valid actions

    def result(self, state, action):
        """
        Return the new state produced by performing an action.

        Example:

            state  = (0, 0)
            action = "RIGHT"

            result = (1, 0)
        """

        # TODO:
        #
        # 1. Extract x and y from state.
        # 2. Check which action was requested.
        # 3. Return the resulting state.

        x, y = state  # get the current coordinates

        if action == "UP":  # moving up decreases y
            return (x, y - 1)

        if action == "DOWN":  # moving down increases y
            return (x, y + 1)

        if action == "LEFT":  # moving left decreases x
            return (x - 1, y)

        if action == "RIGHT":  # moving right increases x
            return (x + 1, y)

        raise ValueError(f"Unknown action: {action}")  # catch invalid actions


# --------------------------------------------------
# CREATE A PROBLEM
# --------------------------------------------------

problem = GridProblem(
    initial=(0, 0),
    goal=(4, 4)
)


# --------------------------------------------------
# EXPLORE THE PROBLEM
# --------------------------------------------------

print("Initial state:", problem.initial)
print("Goal:", problem.goal)


print("\nActions from (0, 0):")

actions = problem.actions((0, 0))

print(actions)


print("\nResults of those actions:")

if actions is not None:
    for action in actions:

        new_state = problem.result(
            (0, 0),
            action
        )

        print(
            action,
            "->",
            new_state
        )


print("\nIs (4, 4) the goal?")

print(
    problem.goal_test((4, 4))
)


# --------------------------------------------------
# REFLECTION QUESTIONS
# --------------------------------------------------

"""
Be ready to discuss:

1. What information is stored in problem.initial?

ANSWER:
The starting state.
Here it is (0, 0).


2. What information is stored in problem.goal?

ANSWER:
The state we want to reach.
Here it is (4, 4).


3. What is the difference between:

       problem.actions(state)

   and:

       problem.result(state, action)

ANSWER:
actions(state) tells us what moves are allowed.
result(state, action) tells us where one move takes us.

Simple:
actions = "What can I do?"
result = "Where do I end up?"


4. Why doesn't Problem know anything about grids?

ANSWER:
Because Problem is a general class.
It can be reused for different problems, not only grids.


5. Why doesn't GridProblem know anything about search?

ANSWER:
GridProblem only describes the grid and its valid moves.
A separate search algorithm decides how to search it.


6. Could the same Problem structure be used for something
   other than a grid?

ANSWER:
Yes.
For example N-Queens, puzzles, games, or route problems.
"""