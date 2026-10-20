"""
AINL3001 — Knowledge-Driven AI
Week 5 — Constraint Satisfaction Problems
BSP 2026

Australian map colouring: six regions and three colours.

Tasks
-----
0. Examine an invalid assignment.
1. Understand variables, domains and constraints.
2. Implement constraint checking.
3. Implement backtracking with simple variable selection.
4. Compare backtracking with brute force.
5. Improve variable selection using MRV.

Work in this starter file and commit your progress to your own fork.
"""

# --------------------------------------------------
# TASK 0 — MANUAL EXPLORATION
# --------------------------------------------------

example_assignment = {
    "WA": "Red",
    "NT": "Red",
    "SA": "Green",
    "Q": "Blue",
    "NSW": "Red",
    "V": "Green",
}

print("Manual CSP Exploration")
print(example_assignment)
print("\nQuestions:")
print("1. Is this assignment valid?")
print("2. Which neighbouring pairs violate a constraint?")
print("3. How could you correct the assignment?")
print("4. Why is it useful to detect violations early?")

"""
TASK 0 ANSWERS

1. No. Some neighbouring regions have the same colour.
2. WA and NT are both Red; SA and V are both Green.
3. Change WA to Blue and V to Blue. All neighbours then differ.
4. Rejecting bad choices early saves checking more invalid assignments.
"""

# --------------------------------------------------
# TASK 1 — CSP REPRESENTATION
# --------------------------------------------------

# Each variable is an Australian region.
variables = ["WA", "NT", "SA", "Q", "NSW", "V"]

# Each region may use one of these three colours.
domains = {
    variable: ["Red", "Green", "Blue"]
    for variable in variables
}

# Each pair of neighbouring regions must have different colours.
constraints = [
    ("WA", "NT"),
    ("WA", "SA"),
    ("NT", "SA"),
    ("NT", "Q"),
    ("SA", "Q"),
    ("SA", "NSW"),
    ("SA", "V"),
    ("Q", "NSW"),
    ("NSW", "V"),
]

"""
TASK 1 ANSWERS

1. A list stores the regions in a fixed order.
2. A dictionary links each region to its possible colours.
3. ("WA", "NT") means these neighbours must have different colours.
4. Add the region to variables, give it a domain, and add its neighbour pairs.
"""

# --------------------------------------------------
# TASK 2 — CONSTRAINT CHECKING
# --------------------------------------------------

def is_valid_assignment(assignment):
    """Return True if a complete OR partial assignment is valid."""
    # TODO:
    # 1. Loop over neighbouring pairs in constraints.
    # 2. If BOTH regions have been assigned, compare their colours.
    # 3. Return False if neighbouring regions have the same colour.
    # 4. Otherwise return True.
    for first, second in constraints:  # check each neighbouring pair
        if first in assignment and second in assignment:  # both have colours
            if assignment[first] == assignment[second]:  # same colour is invalid
                return False  # at least one rule is broken
    return True  # no rule was broken


# --------------------------------------------------
# TASK 3 AND TASK 5 — VARIABLE SELECTION
# --------------------------------------------------

def select_unassigned_variable(assignment):
    """Choose the next unassigned region.

    Task 3: First return the FIRST unassigned region.

    Task 5: Replace that approach with MRV (Minimum Remaining Values):
    choose the unassigned region with the FEWEST currently legal
    colours. Break ties by keeping the first region in variables.
    """
    # TASK 3 TODO:
    # Return the first variable not in assignment, or None if all
    # variables have been assigned.
    #
    # TASK 5 TODO (after backtracking works):
    # For each unassigned variable, temporarily try each colour,
    # check is_valid_assignment(), and undo the temporary assignment.
    # Count legal colours and choose the variable with the fewest.

    unassigned = [var for var in variables if var not in assignment]  # remaining regions

    if not unassigned:  # every region has a colour
        return None

    best_variable = None  # selected region
    fewest_colours = float("inf")  # start with a very large number

    for variable in unassigned:  # check each unassigned region
        legal_colours = 0  # count currently allowed colours

        for colour in domains[variable]:  # temporarily try each colour
            assignment[variable] = colour  # assign colour
            if is_valid_assignment(assignment):  # colour does not break a rule
                legal_colours += 1  # count valid colour
            del assignment[variable]  # undo the trial

        if legal_colours < fewest_colours:  # fewest options so far
            fewest_colours = legal_colours  # remember the count
            best_variable = variable  # remember the region

    return best_variable  # MRV: fewest legal colours, first if tied


# --------------------------------------------------
# TASK 3 — BACKTRACKING SEARCH
# --------------------------------------------------

def backtracking_search(assignment):
    """Return a complete valid assignment, or None if none exists."""
    # TODO:
    # 1. If every variable has been assigned, return a COPY.
    # 2. Choose a variable with select_unassigned_variable().
    # 3. For each colour in its domain, temporarily assign it.
    # 4. If the partial assignment is valid, search recursively.
    # 5. Return the recursive result if a solution was found.
    # 6. Otherwise remove the temporary assignment (backtrack).
    # 7. Return None if every colour fails.

    if len(assignment) == len(variables):  # all regions assigned
        return assignment.copy() if is_valid_assignment(assignment) else None

    variable = select_unassigned_variable(assignment)  # choose the next region

    for colour in domains[variable]:  # try each possible colour
        assignment[variable] = colour  # temporarily colour this region

        if is_valid_assignment(assignment):  # only continue if valid
            result = backtracking_search(assignment)  # solve remaining regions
            if result is not None:  # complete solution found
                del assignment[variable]  # undo temporary change
                return result  # return the solution

        del assignment[variable]  # backtrack and try another colour

    return None  # no colour worked


# --------------------------------------------------
# TASK 4 — BRUTE FORCE COMPARISON
# --------------------------------------------------

# Six regions with three possible colours each give 3 ** 6 = 729
# complete assignments. Why can backtracking avoid checking all 729?

"""
TASK 4 ANSWERS

1. Yes. Brute force includes complete assignments with matching neighbours.
2. Backtracking rejects an invalid partial assignment immediately.
3. It avoids exploring all the ways to finish an already-invalid colouring.
4. No. Our search stops as soon as it finds its first valid solution.

There are 3 ** 6 = 729 possible complete colour assignments.
That does NOT mean 729 valid solutions or 729 backtracking attempts.
"""

# --------------------------------------------------
# TESTING AREA
# --------------------------------------------------

if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("WEEK 5 — CONSTRAINT SATISFACTION PROBLEMS")
    print("=" * 50)

    print("\nVariables:", variables)
    print("Domains:", domains)
    print("Constraints:", constraints)

    print("\nExample assignment valid?")
    print(is_valid_assignment(example_assignment))  # Expected: False

    partial_assignment = {"WA": "Red", "NT": "Green"}
    print("\nPartial assignment valid?")
    print(is_valid_assignment(partial_assignment))  # Expected: True

    print("\nSearching for a solution...")
    solution = backtracking_search({})
    print("Solution:", solution)

    if solution is not None:
        print("\nSolution valid?", is_valid_assignment(solution))
        print("\nColour assignment:")
        for region in variables:
            print(f"{region:4} -> {solution[region]}")
    else:
        print("No solution yet. Complete the TODO sections.")

    print("\nPossible complete assignments:", 3 ** len(variables))
    print("\nReflection:")
    print("1. What causes backtracking?")
    print("2. Why can backtracking be faster than brute force?")
    print("3. Why might MRV reduce search?")
    print("4. How could this model represent timetabling?")