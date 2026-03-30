import logging
import math

def greedy(maze: list[list], start: tuple, finish: tuple):
    cur_pos = start
    steps = 0
    viz: list[tuple] = []  
    position_stack = []  
    position_stack.append(cur_pos)

    prioritized_direcitons: list[tuple] = []
    while cur_pos != finish:
        prioritized_direcitons = list_best_directions_based_on_heuristic(cur_pos, finish)  

        break_happened = False
        direction_to_move = (0, 0)
        for direction in prioritized_direcitons:  
            move_legal = True
            if not (0 <= cur_pos[0] + direction[0] < len(maze)):
                print("aa")
                move_legal = False

            if not (0 <= cur_pos[1] + direction[1] < len(maze[0])):
                print("bb")
                move_legal = False

            if move_legal and maze[cur_pos[0] + direction[0]][cur_pos[1] + direction[1]] == 1:  
                print("cc")
                move_legal = False

            if move_legal and (cur_pos[0] + direction[0], cur_pos[1] + direction[1]) in viz:
                move_legal = False

            if move_legal:
                break_happened = True

                direction_to_move = direction
                break

        if break_happened:  
            steps += 1
            cur_pos = (cur_pos[0] + direction_to_move[0], cur_pos[1] + direction_to_move[1])
            position_stack.append(cur_pos)  
            viz.append(cur_pos)  
            print(f"MOVED TO {cur_pos}")

        else:  
            if len(position_stack) == 0:
                steps = -1
                break  
            cur_pos = position_stack.pop()

    return steps, viz

def list_best_directions_based_on_heuristic(start: tuple, end: tuple) -> list[tuple]:
    directions = [(1, 0), (0, -1), (-1, 0), (0, 1)]

    scored_directions = []

    for d in directions:
        new_pos = (start[0] + d[0], start[1] + d[1])
        score = h1_manhattan(new_pos, end)  
        scored_directions.append((score, d))

    scored_directions.sort(key=lambda x: x[0])

    return [direction for score, direction in scored_directions]

def h1_manhattan(start: tuple, end: tuple) -> int:
    return abs(start[0] - end[0]) + abs(start[1] - end[1])

def h2_eucledian() -> list[tuple]:
    pass

def vizualize(viz: list[tuple]):
    pass

def get_distance(p1, p2):
    x1 = p1[0]
    y1 = p1[1]
    x2 = p2[0]
    y2 = p2[1]
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def solve_maze_greedy(maze, start, end):
    curr = start
    path = [start]
    visited = [start]
    
    print("--- STARTING SEARCH ---")
    
    while curr != end:
        for r in range(len(maze)):
            row_str = ""
            for c in range(len(maze[0])):
                if (r, c) == curr:
                    row_str += " @ "
                elif (r, c) == start:
                    row_str += " S "
                elif (r, c) == end:
                    row_str += " G "
                elif maze[r][c] == 1:
                    row_str += " # "
                elif (r, c) in visited:
                    row_str += " . "
                else:
                    row_str += " - "
            print(row_str)
        print("-" * 15)

        x = curr[0]
        y = curr[1]
        neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        
        best_node = None
        best_dist = 1000000 
        
        for n in neighbors:
            nx = n[0]
            ny = n[1]
            
            if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]):

                if maze[nx][ny] == 0 and n not in visited:
                    d = get_distance(n, end)
                    if d < best_dist:
                        best_dist = d
                        best_node = n
        
        if best_node is not None:
            curr = best_node
            visited.append(curr)
            path.append(curr)
            print(f"Moving to: {curr}")
        else:
            if len(path) > 1:
                print("Stuck! Backtracking...")
                path.pop()
                curr = path[-1]
            else:
                print("No path possible!")
                return -1
                
    print("GOAL REACHED!")
    return len(path) - 1

maze = [[0, 1, 0, 0, 0], [0, 1, 0, 1, 0], [0, 0, 0, 1, 0], [1, 0, 1, 0, 0], [0, 0, 0, 1, 0]]
start_position = (0, 0)
finish_position = (4, 4)

print("Running first implementation (greedy):")
num_steps, viz = greedy(maze, start_position, finish_position)
if num_steps != -1:
    print(f"Path from {start_position} to {finish_position} is {num_steps} steps.")
else:
    print(f"No path from {start_position} to {finish_position} exists.")
vizualize(viz)

print("\nRunning second implementation (solve_maze_greedy):")
steps = solve_maze_greedy(maze, start_position, finish_position)
print("Final Score (Steps):", steps)
