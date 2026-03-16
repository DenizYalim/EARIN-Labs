import logging

""" EDGE CASES
* finish line might not be accesible from start
* start might be enclosed by walls at every direction

"""

"""
Greedy best-first search

Parameters:
- maze: The 2D matrix that represents the maze with 0 represents empty space and 1 represents a wall
- start: A tuple with the coordinates of starting position
- finish: A tuple with the coordinates of finishing position

Returns:
- Number of steps from start to finish, equals -1 if the path is not found
- Viz - everything required for step-by-step vizualization

"""


def greedy(maze: list[list], start: tuple, finish: tuple):
    cur_pos = start
    steps = 0
    viz: list[tuple] = []  # will add current positions to here
    position_stack = []  # will hold positions been in; will be used for backtracking
    position_stack.append(cur_pos)

    prioritized_direcitons: list[tuple] = []
    while cur_pos != finish:
        prioritized_direcitons = list_best_directions_based_on_heuristic(cur_pos, finish)  # get directions in order of best to worst based on heuristic

        # check if moving is out of index
        break_happened = False
        direction_to_move = (0, 0)
        for direction in prioritized_direcitons:  # check 4 sides of you, in priorities
            move_legal = True
            if not (0 <= cur_pos[0] + direction[0] < len(maze)):
                print("aa")
                move_legal = False

            if not (0 <= cur_pos[1] + direction[1] < len(maze[0])):
                print("bb")
                move_legal = False

            # check if there is a wall there
            if move_legal and maze[cur_pos[0] + direction[0]][cur_pos[1] + direction[1]] == 1:  # 1 means wall
                print("cc")
                move_legal = False

            # check if that cell was visited before, if so don't go there
            if move_legal and (cur_pos[0] + direction[0], cur_pos[1] + direction[1]) in viz:
                move_legal = False

            if move_legal:
                break_happened = True

                direction_to_move = direction
                break

        if break_happened:  # move
            steps += 1
            cur_pos = (cur_pos[0] + direction_to_move[0], cur_pos[1] + direction_to_move[1])
            position_stack.append(cur_pos)  #  TODO appends to the end right?
            viz.append(cur_pos)  # visited
            print(f"MOVED TO {cur_pos}")

        else:  # break didn't happen; backtrack!
            # position_stack.pop()
            if len(position_stack) == 0:
                steps = -1
                break  # maze isn't solvable
            cur_pos = position_stack.pop()

    return steps, viz


import math


def list_best_directions_based_on_heuristic(start: tuple, end: tuple) -> list[tuple]:
    directions = [(1, 0), (0, -1), (-1, 0), (0, 1)]

    scored_directions = []

    for d in directions:
        new_pos = (start[0] + d[0], start[1] + d[1])
        score = h1_manhattan(new_pos, end)  # get manhattan score of all
        scored_directions.append((score, d))

    scored_directions.sort(key=lambda x: x[0])

    return [direction for score, direction in scored_directions]


def h1_manhattan(start: tuple, end: tuple) -> int:
    return abs(start[0] - end[0]) + abs(start[1] - end[1])


def h2_eucledian() -> list[tuple]:
    pass


def vizualize(viz: list[tuple]):
    """
    Vizualization function. Shows step by step the work of the search algorithm

    Parameters:
    - viz: everything required for step-by-step vizualization
    """

    """
    for list in maze:
        for tile in list:
            if tile == 0:
                print("_", end="")
            else:
                print("#", end="")
        print()
        """


# Example usage:
maze = [[0, 1, 0, 0, 0], [0, 1, 0, 1, 0], [0, 0, 0, 1, 0], [1, 0, 1, 0, 0], [0, 0, 0, 1, 0]]

start_position = (0, 0)
finish_position = (4, 4)

num_steps, viz = greedy(maze, start_position, finish_position)

# Print number of steps in path
if num_steps != -1:
    print(f"Path from {start_position} to {finish_position} using greedy best-first search is {num_steps} steps.")

else:
    print(f"No path from {start_position} to {finish_position} exists.")

# Vizualize algorithm step-by-step even if the path was not found
vizualize(viz)
