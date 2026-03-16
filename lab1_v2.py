import logging

""" EDGE CASES
* finish line might not be accesible from start
* start might be enclosed by walls at every direction

"""


def greedy(maze: list[list], start: tuple, finish: tuple):
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
