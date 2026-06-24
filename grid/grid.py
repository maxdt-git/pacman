import pygame
from mazegenerator.mazegenerator import MazeGenerator


def draw_cell(hex: int, x: int, y: int) -> list[pygame.Rect]:
    """
    Draw a cell, wall by wall using the binary of the number of the cell,
    0101 = WestSouthEastNorth, 1 is a close wall and 0 an open

    Arguments:
    hex -- value of the cell
    x -- width pos
    y -- height pos
    """
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8
    CELL_SIZE = 48
    WALL_THICK = 4
    cell: list[pygame.Rect] = []
    if hex == 15:
        rectry0: pygame.Rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        cell.append(rectry0)
    if hex & NORTH:
        rectry1: pygame.Rect = pygame.Rect(x, y, CELL_SIZE, WALL_THICK)
        cell.append(rectry1)
    if hex & EAST:
        rectry2: pygame.Rect = pygame.Rect(
            x + CELL_SIZE - WALL_THICK, y, WALL_THICK, CELL_SIZE)
        cell.append(rectry2)
    if hex & SOUTH:
        rectry3: pygame.Rect = pygame.Rect(
            x, y + CELL_SIZE - WALL_THICK, CELL_SIZE, WALL_THICK)
        cell.append(rectry3)
    if hex & WEST:
        rectry4: pygame.Rect = pygame.Rect(x, y, WALL_THICK, CELL_SIZE)
        cell.append(rectry4)
    return cell


def draw_all(seednb: int) -> tuple[
        list[list[pygame.Rect]], int, int, list[list[int]]]:
    """
    Draw all the maze and returns a tuple of the grid, distance between the
    window and the maze (x and y), and the maze generated in list[list[int]]

    Arguments:
    seednb -- define the seed of the maze
    """
    if seednb:
        gen = MazeGenerator(seed=seednb)
    else:
        gen = MazeGenerator()
    maze = gen.maze

    CELL_SIZE = 48
    WALL_THICK = 4
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 800

    maze_rows = len(maze)
    maze_cols = len(maze[0])
    step = CELL_SIZE - WALL_THICK
    maze_pixel_width = CELL_SIZE + (maze_cols - 1) * step
    maze_pixel_height = CELL_SIZE + (maze_rows - 1) * step
    offsetx = (SCREEN_WIDTH - maze_pixel_width) // 2
    offsety = (SCREEN_HEIGHT - maze_pixel_height) // 2

    grid: list[list[pygame.Rect]] = []
    y = offsety
    for row in maze:
        x = offsetx
        for cell in row:
            cur = draw_cell(cell, x, y)
            grid.append(cur)
            x += step
        y += step
    return grid, offsetx, offsety, gen.maze


def open_cells(maze: list[list[int]]) -> list[tuple[int, int]]:
    """
    Find the cell of the maze we can use to place the pacgums

    Arguments:
    maze -- the generated maze, in list[[list[int]] version
    """
    pos_list: list[tuple[int, int]] = []
    for i in range(len(maze[0])):
        for j in range(len(maze[0])):
            if not maze[i][j] == 15:
                if (i == 0 and j == 0) or (
                    i == 0 and j == 14) or (
                        i == 14 and j == 0) or (
                            i == 14 and j == 14):
                    continue
                cell = (i, j)
                pos_list.append(cell)
    return pos_list
