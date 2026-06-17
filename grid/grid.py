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


def draw_all(seednb: int) -> list[list[pygame.Rect]]:
    if seednb:
        gen = MazeGenerator(seed=seednb)
    else:
        gen = MazeGenerator()
    maze = gen.maze
    grid: list[list[pygame.Rect]] = []
    x = 70
    y = 50
    for row in maze:
        for cell in row:
            cur = draw_cell(cell, x, y)
            grid.append(cur)
            x += 48 - 4
        x -= (48 - 4) * len(row)
        y += 48 - 4
    return grid
