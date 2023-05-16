import settings
import pygame as pg
from random import random
from collections import deque
import breadth_first_search as bfs
cols, rows = settings.cols, settings.rows
TILE = settings.TILE


pg.init()
sc = pg.display.set_mode([cols * TILE + 5 * TILE, rows * TILE])
clock = pg.time.Clock()

# Builds 2d Array of 1 and 0 used to add blocks
grid = [[1 if random() < settings.wall_percentage and col != 0 and row != 0 else 0 for col in range(cols)] for row in range(rows)]


def get_rect(x, y):
    return x * TILE + 1, y * TILE + 1, TILE - 2, TILE - 2


def get_next_nodes(x, y):
    # Check_adjacent_nodes checks if adjacent cell is in the visible grid and if it's not an obstacle
    # Range returns cols/rows - 1 as last index
    check_adjacent_node = lambda x, y: True if 0 <= x < cols and 0 <= y < rows and not grid[y][x] else False
    return [(x + dx, y + dy) for dx, dy in settings.bfs_directions if check_adjacent_node(x + dx, y + dy)]

def  draw_bfs():
    [pg.draw.rect(sc, pg.Color('darkgreen'), get_rect(x, y)) for x, y in visited]
    [pg.draw.rect(sc, pg.Color('darkslategray'), get_rect(x, y)) for x, y in queue]
    # the gone_path stays as it is not overwritten
    path_head, gone_path = goal, goal
    while gone_path and gone_path in visited:
        pg.draw.rect(sc, pg.Color('white'), get_rect(*gone_path), TILE, border_radius=TILE // 5)
        gone_path = visited[gone_path]
    pg.draw.rect(sc, pg.Color('blue'), get_rect(*start), TILE, border_radius=TILE // 3)
    pg.draw.rect(sc, pg.Color('red'), get_rect(*path_head), border_radius=TILE // 3)



graph = {}
for y, row in enumerate(grid):
    for x, col in enumerate(row):
        if not col:
            # Adds all adjacent cells to the Dictionary
            graph[(x, y)] = graph.get((x, y), []) + get_next_nodes(x, y)


# Breadth-First-Search Init
start = (0, 0)
goal = start
queue = deque([start])
visited = {start: None}
cur_node = start



def get_mouse_pos_onclick():
    x, y = pg.mouse.get_pos()
    grid_x, grid_y = x // TILE, y // TILE
    if grid_x < cols and grid_y < rows:
        pg.draw.rect(sc, pg.Color('orange'), get_rect(grid_x, grid_y))
    click = pg.mouse.get_pressed()
    return (grid_x, grid_y) if click[0] and grid_x < cols and grid_y < rows else False

finished = False
while True:
    sc.fill(pg.Color('White'))
    # Draw Grid
    for y, row in enumerate(grid):
        for x, col in enumerate(row):
            if col == 1:
                pg.draw.rect(sc, pg.Color('black'), get_rect(x, y), border_radius=TILE // 5)
            else:
                pg.draw.rect(sc, pg.Color('grey'), get_rect(x, y), border_radius=0)


    mouse_pos = get_mouse_pos_onclick()
    if settings.algorithm == 'BFS':
        if settings.fast_mode:
            if mouse_pos and not grid[mouse_pos[1]][mouse_pos[0]]:
                goal = mouse_pos
                queue, visited = bfs.fast_bfs(start, goal, graph)
        else:
            if not finished:
                if mouse_pos and not grid[mouse_pos[1]][mouse_pos[0]]:
                    goal = mouse_pos
                    finished, queue, visited = bfs.slow_bfs(start, goal, graph, queue, visited)
            # Should be repeated as long mouse is held
            elif mouse_pos:
                queue = deque([start])
                visited = {start: None}
                finished = False
        draw_bfs()


    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
    pg.display.flip()
    clock.tick(60)
