import pygame as pg
from grid import draw_all
import random


# class Pacman():
#     def __init__(self, width: int, height: int) -> None:
#         self.image = pg.transform.scale(
#             pg.image.load('assets/pacman.png'), (30, 30))
#         self.rect = self.image.get_rect()
#         self.rect.topleft = (width // 2, height // 2)
#         self.pos_x = float(width // 2)
#         self.pos_y = float(height // 2)
#         self.score = 0
#         self.angle = 0
#         self.rot = pg.transform.rotate(self.image, self.angle)


class Ghosts():
    CELL_SIZE = 48
    WALL_THICK = 4
    STEP = CELL_SIZE - WALL_THICK
    PAC_SIZE = 20
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 800
    MAZE_ROWS = 15
    MAZE_COLS = 15
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8

    def __init__(
            self, offset_x: int, offset_y: int, maze: list[
                list[int]], row: int = 0, col: int = 0) -> None:
        self.row = row
        self.col = col
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.lastmove = pg.time.get_ticks()
        self.rect = self.create()
        self.direction = self.chose_direction(maze)

    def chose_direction(self, maze: list[list[int]]) -> str:
        available: list[str] = []
        if not maze[self.row][self.col] & self.NORTH:
            available.append("N")
        if not maze[self.row][self.col] & self.EAST:
            available.append("E")
        if not maze[self.row][self.col] & self.SOUTH:
            available.append("S")
        if not maze[self.row][self.col] & self.WEST:
            available.append("W")
        dir = random.choice(available)
        return dir

    def update(self, maze: list[list[int]]) -> None:
        time = pg.time.get_ticks()
        if time - self.lastmove >= 500:
            self.move(maze)
            self.lastmove = time

    def create(self) -> pg.Rect:
        x = self.offset_x + self.col * self.STEP + self.CELL_SIZE // 2
        y = self.offset_y + self.row * self.STEP + self.CELL_SIZE // 2
        rect = pg.Rect(0, 0, self.PAC_SIZE, self.PAC_SIZE)
        rect.center = (x, y)
        return rect

    def move(self, maze: list[list[int]]) -> None:
        # should maybe change direction for each intersection
        if self.direction == "S" and maze[self.row][self.col] & self.SOUTH:
            self.direction = self.chose_direction(maze)
        if self.direction == "N" and maze[self.row][self.col] & self.NORTH:
            self.direction = self.chose_direction(maze)
        if self.direction == "E" and maze[self.row][self.col] & self.EAST:
            self.direction = self.chose_direction(maze)
        if self.direction == "W" and maze[self.row][self.col] & self.WEST:
            self.direction = self.chose_direction(maze)

        if self.direction == "S" and not maze[self.row][self.col] & self.SOUTH:
            self.row += 1
            self.rect = self.create()
        if self.direction == "N" and not maze[self.row][self.col] & self.NORTH:
            self.row -= 1
            self.rect = self.create()
        if self.direction == "E" and not maze[self.row][self.col] & self.EAST:
            self.col += 1
            self.rect = self.create()
        if self.direction == "W" and not maze[self.row][self.col] & self.WEST:
            self.col -= 1
            self.rect = self.create()


class Pac():
    CELL_SIZE = 48
    WALL_THICK = 4
    STEP = CELL_SIZE - WALL_THICK
    PAC_SIZE = 20
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 800
    MAZE_ROWS = 15
    MAZE_COLS = 15
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8

    def __init__(self, offset_x: int, offset_y: int) -> None:
        self.row = self.MAZE_ROWS // 2
        self.col = self.MAZE_COLS // 2
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.rect = self.create(self.row, self.col)

    def create(self, row: int, col: int) -> pg.Rect:
        x = self.offset_x + col * self.STEP + self.CELL_SIZE // 2
        y = self.offset_y + row * self.STEP + self.CELL_SIZE // 2
        rect = pg.Rect(0, 0, self.PAC_SIZE, self.PAC_SIZE)
        rect.center = (x, y)
        return rect

    def move(self, key: int, maze: list[list[int]]) -> None:
        if key == pg.K_UP and not maze[self.row][self.col] & self.NORTH:
            self.row -= 1
        elif key == pg.K_DOWN and not maze[self.row][self.col] & self.SOUTH:
            self.row += 1
        elif key == pg.K_RIGHT and not maze[self.row][self.col] & self.EAST:
            self.col += 1
        elif key == pg.K_LEFT and not maze[self.row][self.col] & self.WEST:
            self.col -= 1
        self.rect = self.create(self.row, self.col)

    def check_collide(
            self, g1: pg.Rect, g2: pg.Rect, g3: pg.Rect, g4: pg.Rect) -> bool:
        if self.rect.colliderect(g1):
            return True
        if self.rect.colliderect(g2):
            return True
        if self.rect.colliderect(g3):
            return True
        if self.rect.colliderect(g4):
            return True
        return False


class Game():
    def __init__(self) -> None:
        self.screen = pg.display.set_mode((800, 800))
        self.name = pg.display.set_caption("Pac-Man")
        self.font = pg.font.Font("fonts/Pixeltype.ttf", 50)
        self.text_surface = self.font.render("score", False, "White")
        self.allcells, self.offset_x, self.offset_y, self.maze = draw_all(0)


class Run():
    def __init__(self) -> None:
        self.life = 3
        self.score = 0
