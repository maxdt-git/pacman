import pygame as pg
from grid import draw_all


class Pacman():
    def __init__(self, width: int, height: int) -> None:
        self.image = pg.transform.scale(
            pg.image.load('assets/pacman.png'), (30, 30))
        self.rect = self.image.get_rect()
        self.rect.topleft = (width // 2, height // 2)
        self.pos_x = float(width // 2)
        self.pos_y = float(height // 2)
        self.score = 0
        self.angle = 0
        self.rot = pg.transform.rotate(self.image, self.angle)


class Ghosts():
    def __init__(self, x: int, y: int) -> None:
        self.image = pg.transform.scale(
            pg.image.load('assets/ghosts.png'), (30, 30))
        self.rect = self.image.get_rect()
        self.pos_x = x
        self.pos_y = y


class Game():
    def __init__(self) -> None:
        self.screen = pg.display.set_mode((800, 800))
        self.name = pg.display.set_caption("Pac-Man")
        self.font = pg.font.Font("fonts/Pixeltype.ttf", 50)
        self.text_surface = self.font.render("score", False, "White")
        self.allcells = draw_all(0)
