cols, rows = 25, 30
TILE = (18750 // (cols*rows))
x_y_directions = [-1, 0], [0, -1], [1, 0], [0, 1]
dia_directions = [1, 1], [-1, 1], [-1, -1], [1, -1]
bfs_directions = x_y_directions + dia_directions
wall_percentage = 0.5
fast_mode = False
algorithm = 'BFS'