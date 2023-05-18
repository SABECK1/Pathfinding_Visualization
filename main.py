import settings
import pygame as pg
from random import random
from collections import deque
import breadth_first_search as bfs

cols, rows = settings.cols, settings.rows
TILE = settings.TILE

pg.init()
sc = pg.display.set_mode([cols * TILE + 7 * TILE, rows * TILE])
pg.display.set_caption("Breadth-First-Search Demonstration")
clock = pg.time.Clock()
font = pg.font.Font('freesansbold.ttf', 23)

# Builds 2d Array of 1 and 0 used to add blocks
grid = [[1 if random() < settings.wall_percentage and col != 0 and row != 0 else 0 for col in range(cols)] for row in
        range(rows)]


# Tilegeneration
def get_rect(x, y):
    return x * TILE + 1, y * TILE + 1, TILE - 2, TILE - 2


# Buttongeneration
def get_button(x, y):
    return x * TILE + TILE, y * TILE + 1, 5 * TILE, 1.5 * TILE


def create_text(text, button_coords):
    text = font.render(text, True, 'black')
    text_rect = text.get_rect()
    # text_rect.left = button_coords[0]
    # text_rect.top = button_coords[1]
    text_rect.center = (button_coords[0] + button_coords[2] // 2, button_coords[1] + button_coords[3] // 2)
    sc.blit(text, text_rect)


def get_next_nodes(x, y):
    # Check_adjacent_nodes checks if adjacent cell is in the visible grid and if it's not an obstacle
    # Range returns cols/rows - 1 as last index
    check_adjacent_node = lambda x, y: True if 0 <= x < cols and 0 <= y < rows and not grid[y][x] else False
    return [(x + dx, y + dy) for dx, dy in settings.bfs_directions if check_adjacent_node(x + dx, y + dy)]


def draw_bfs():
    [pg.draw.rect(sc, pg.Color('darkgreen'), get_rect(x, y)) for x, y in visited]
    [pg.draw.rect(sc, pg.Color('darkslategray'), get_rect(x, y)) for x, y in queue]
    # the gone_path stays as it is not overwritten
    path_head, gone_path = goal, goal
    while gone_path and gone_path in visited:
        pg.draw.rect(sc, pg.Color('white'), get_rect(*gone_path), TILE, border_radius=TILE // 5)
        gone_path = visited[gone_path]
    pg.draw.rect(sc, pg.Color('blue'), get_rect(*start), TILE, border_radius=TILE // 3)
    pg.draw.rect(sc, pg.Color('red'), get_rect(*path_head), border_radius=TILE // 3)

def reset_bfs():
    queue = deque([start])
    visited = {start: None}
    return queue, visited


def create_graph():
    graph = {}
    for y, row in enumerate(grid):
        for x, col in enumerate(row):
            if not col:
                # Adds all adjacent cells to the Dictionary
                graph[(x, y)] = graph.get((x, y), []) + get_next_nodes(x, y)
    return graph

graph = create_graph()

# Breadth-First-Search Init
start = (0, 0)
goal = start
queue = deque([start])
visited = {start: None}
cur_node = start

button0 = get_button(cols, 2)
button1 = get_button(cols, 5)
button2 = get_button(cols, 8)
button3 = get_button(cols, 11)
buttons = [button0, button1, button2, button3]


def get_mouse_pos_onclick():
    x, y = pg.mouse.get_pos()
    grid_x, grid_y = x // TILE, y // TILE
    if grid_x < cols and grid_y < rows:
        pg.draw.rect(sc, pg.Color('orange'), get_rect(grid_x, grid_y))
    click = pg.mouse.get_pressed()
    return (grid_x, grid_y) if (click[0] or click[2]) and grid_x < cols and grid_y < rows else False


def get_mouse_pos():
    x, y = pg.mouse.get_pos()
    return x, y


finished = False
hover_button_idx = None
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

    # Initial Button Color
    [pg.draw.rect(sc, pg.Color('grey'), button) for button in buttons]

    # Button Hover Color
    for idx, button in enumerate(buttons):
        if button[0] < get_mouse_pos()[0] < button[0] + button[2] and button[1] < get_mouse_pos()[1] < button[1] + \
                button[3]:
            pg.draw.rect(sc, pg.Color('red'), button)
            hover_button_idx = idx

    create_text('FastMode', buttons[0])
    create_text('SlowMode', buttons[1])
    create_text('Reset', buttons[2])
    create_text('Diagonal', buttons[3])

    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()

        # Leftclick
        # When Mode is switched additionally reset the algorithm
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if hover_button_idx == 0:
                settings.fast_mode = True
                queue, visited = reset_bfs()
            elif hover_button_idx == 1:
                settings.fast_mode = False
                queue, visited = reset_bfs()
            elif hover_button_idx == 2:
                grid = [[0 for col in range(cols)] for row in range(rows)]
                graph = create_graph()
                queue, visited = reset_bfs()
            elif hover_button_idx == 3:
                if settings.bfs_directions == settings.x_y_directions + settings.dia_directions:
                    settings.bfs_directions = settings.x_y_directions
                else:
                    settings.bfs_directions = settings.x_y_directions + settings.dia_directions
                queue, visited = reset_bfs()
                graph = create_graph()


        # Resets hoverbutton so it doesn't register event twice
        hover_button_idx = None
        # Rightclick
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
            mouse_pos = get_mouse_pos_onclick()
            if mouse_pos:
                cl_x, cl_y = get_mouse_pos_onclick()
                grid[cl_y][cl_x] = 1
                graph = create_graph()


    pg.display.flip()
    clock.tick(60)
