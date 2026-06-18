import pygame
from mazegenerator.mazegenerator import MazeGenerator  # type: ignore


def draw_cell(hex: int, x: int, y: int) -> list[pygame.Rect]:
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8
    CELL_SIZE = 48
    WALL_THICK = 4
    cell: list[pygame.Rect] = []
    if hex == 15:
        rectry: pygame.Rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        cell.append(rectry)
    if hex & NORTH:
        rectry: pygame.Rect = pygame.Rect(x, y, CELL_SIZE, WALL_THICK)
        cell.append(rectry)
    if hex & EAST:
        rectry: pygame.Rect = pygame.Rect(
            x + CELL_SIZE - WALL_THICK, y, WALL_THICK, CELL_SIZE)
        cell.append(rectry)
    if hex & SOUTH:
        rectry: pygame.Rect = pygame.Rect(
            x, y + CELL_SIZE - WALL_THICK, CELL_SIZE, WALL_THICK)
        cell.append(rectry)
    if hex & WEST:
        rectry: pygame.Rect = pygame.Rect(x, y, WALL_THICK, CELL_SIZE)
        cell.append(rectry)
    return cell


def draw_all(seednb: int) -> tuple[
        list[list[pygame.Rect]], int, int, list[list[int]]]:
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
