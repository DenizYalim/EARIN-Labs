# this solution doesn't work --   my bad -deniz
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
    directions = [(1, 0), (0, -1), (-1, 0), (0, 1)]
    directions_num = 0
    cur_dir = directions[0]
    cur_pos = start
    steps = 0
    viz: list[tuple] = []  # will add current positions to here

    while cur_pos != finish:
        if steps % 100 == 0 and steps > 100:
            logging.info(f"step count: {steps}")
        move_legal = True
        # check if moving is out of index
        if not (0 <= cur_pos[0] + cur_dir[0] < len(maze)):
            print("aa")
            move_legal = False

        if not (0 <= cur_pos[1] + cur_dir[1] < len(maze[0])):
            print("bb")
            move_legal = False

        # check if there is a wall there
        if move_legal and maze[cur_pos[0] + cur_dir[0]][cur_pos[1] + cur_dir[1]] == 1:  # 1 means wall
            print("cc")
            move_legal = False

        # check if that cell was visited before, if so don't go there
        if move_legal and (cur_pos[0] + cur_dir[0], cur_pos[1] + cur_dir[1]) in viz:
            move_legal = False

        if move_legal:
            steps += 1
            cur_pos = (cur_pos[0] + cur_dir[0], cur_pos[1] + cur_dir[1])
            viz.append(cur_pos)
            print(f"MOVED TO {cur_pos}")
        else:  # IF CANNOT MOVE THERE, change directions!
            cur_dir = directions[directions_num]
            directions_num = (directions_num + 1) % 4

    return steps, viz
