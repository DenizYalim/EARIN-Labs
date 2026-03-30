import logging
import math


def greedy(maze: list[list], start: tuple, finish: tuple):
    cur_pos = start
    # steps = 0
    viz: list[tuple] = [start]  # i should probably add start to here as well
    position_stack = []
    position_stack.append(cur_pos)

    prioritized_direcitons: list[tuple] = []
    while cur_pos != finish:
        prioritized_direcitons = list_best_directions_based_on_heuristic(cur_pos, finish)

        break_happened = False
        direction_to_move = (0, 0)
        for direction in prioritized_direcitons:
            move_legal = True
            if not (0 <= cur_pos[0] + direction[0] < len(maze)):  # if outside
                # print("aa")
                move_legal = False

            if not (0 <= cur_pos[1] + direction[1] < len(maze[0])):  # if outside
                # print("bb")
                move_legal = False

            if move_legal and maze[cur_pos[0] + direction[0]][cur_pos[1] + direction[1]] == 1:  # if wall
                # print("cc")
                move_legal = False

            if move_legal and (cur_pos[0] + direction[0], cur_pos[1] + direction[1]) in viz:  # if visited already
                move_legal = False

            if move_legal:
                break_happened = True

                direction_to_move = direction
                break

        if break_happened:
            # steps += 1
            cur_pos = (cur_pos[0] + direction_to_move[0], cur_pos[1] + direction_to_move[1])
            position_stack.append(cur_pos)
            viz.append(cur_pos)
            # print(f"MOVED TO {cur_pos}")

        else:
            if len(position_stack) == 0:
                # steps = -1  # solution is unreachable; set steps to -1, as instructed
                return -1, viz
            cur_pos = position_stack.pop()
            viz.append(cur_pos)

    return len(position_stack), viz
    # return steps, viz


def list_best_directions_based_on_heuristic(start: tuple, end: tuple) -> list[tuple]:
    directions = [(1, 0), (0, -1), (-1, 0), (0, 1)]

    scored_directions = []

    for d in directions:
        new_pos = (start[0] + d[0], start[1] + d[1])
        score = h1_manhattan(new_pos, end)
        scored_directions.append((score, d))

    def repack_scores(pair):
        key, value = pair
        return key

    scored_directions.sort(key=repack_scores)

    return [direction for score, direction in scored_directions]


def h1_manhattan(start: tuple, end: tuple) -> int:  # ||x1-x2|| + ||y1-y2||
    return abs(start[0] - end[0]) + abs(start[1] - end[1])


def vizualize(viz: list[tuple], maze: list[list], finish: tuple = None):
    steps = 0

    for p1, p2 in viz:
        steps += 1
        print(f"\n{steps}")
        temp_maze = [maze[i][:] for i in range(len(maze))]  # needed deep copy
        temp_maze[p1][p2] = "@"
        temp_maze[finish[0]][finish[1]] = "F"
        print_maze(temp_maze)


def print_maze(maze: list[list]):
    for listy in maze:
        print(listy)


"""def h2_eucledian() -> list[tuple]:
    pass"""


maze = [[0, 1, 0, 0, 0], [0, 1, 0, 1, 0], [0, 0, 0, 1, 0], [1, 0, 1, 0, 0], [0, 0, 0, 1, 0]]
start_position = (0, 0)
finish_position = (4, 4)

print("Running first implementation (greedy):")
num_steps, viz = greedy(maze, start_position, finish_position)
vizualize(viz, maze, finish_position)
if num_steps != -1:
    print(f"\n\nPath from {start_position} to {finish_position} takes {num_steps} steps.")
else:
    print(f"No path from {start_position} to {finish_position} exists.")
