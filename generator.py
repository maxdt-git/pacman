import pygame as pg
from grid import draw_all
import random
from parsing import Config
from grid import open_cells
from path_mgmt import (
    pacman_path, pink_path, red_path, orange_path, blue_path, font_path)


class Gum():
    """
    Represents all the values of a gum and method to create it

    Arguments:
    offset_x -- offset x of the grid in the screen to center it
    offset_y -- offset y of the grid in the screen to center it
    row, col -- position of the gum in grid
    rect -- rectangle object with coordinates and size
    exists -- check for drawing
    """
    CELL_SIZE = 48
    WALL_THICK = 4
    STEP = CELL_SIZE - WALL_THICK
    GUM_SIZE = 4

    def __init__(self, offset_x: int, offset_y: int,
                 row: int = 0, col: int = 0):
        """
        initializes each instance with passed values and calls create
        """
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.row = row
        self.col = col
        self.rect = self.create()
        self.exists = True

    def create(self) -> pg.Rect:
        """
        creates a pygame rect with defined size and calculated x, y
        position based on the initial offset and cell sizes, in order
        to center it
        """
        x = self.offset_x + self.col * self.STEP + self.CELL_SIZE // 2
        y = self.offset_y + self.row * self.STEP + self.CELL_SIZE // 2
        rect = pg.Rect(x, y, self.GUM_SIZE, self.GUM_SIZE)
        rect.center = (x, y)
        return rect


class MegaGum():
    """
    Represents all the values of a megagum and method to create it

    Arguments:
    offset_x -- offset x of the grid in the screen to center it
    offset_y -- offset y of the grid in the screen to center it
    row, col -- position of the gum in grid
    rect -- rectangle object with coordinates and size
    exists -- check for drawing
    """
    CELL_SIZE = 48
    WALL_THICK = 4
    STEP = CELL_SIZE - WALL_THICK
    GUM_SIZE = 8

    def __init__(
            self, offset_x: int, offset_y: int,
            row: int = 0, col: int = 0) -> None:
        """
        initializes each instance with passed values and calls create
        """
        self.row = row
        self.col = col
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.rect = self.create()
        self.exists = True

    def create(self) -> pg.Rect:
        """
        creates a pygame rect with defined size and calculated x, y
        position based on the initial offset and cell sizes, in order
        to center it
        """
        x = self.offset_x + self.col * self.STEP + self.CELL_SIZE // 2
        y = self.offset_y + self.row * self.STEP + self.CELL_SIZE // 2
        rect = pg.Rect(x, y, self.GUM_SIZE, self.GUM_SIZE)
        rect.center = (x, y)
        return rect


class Ghosts():
    """
    Represents all the values of a Ghost and method to create it,
    update it, make it move

    Arguments:
    offset_x -- offset x of the grid in the screen to center it
    offset_y -- offset y of the grid in the screen to center it
    row, col -- position of the gum in grid
    base row, col -- position of the gum in grid at creation
    rect -- rectangle object with coordinates and size
    exists -- check for drawing
    lastmove -- tick of last move to calculate next call of move
    last_direction -- last coordinate in the grid to be used in later func
    direction -- current direction toward which to go
    lastdeath -- tick of lastdeath to calculate respawn
    collision -- bool indicating a collision with pac-man
    base_image, image -- used in displaying sprite png
    pos -- used to calculate position relative to pacman's
    """
    CELL_SIZE = 48
    WALL_THICK = 4
    STEP = CELL_SIZE - WALL_THICK
    PAC_SIZE = 20
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8

    def __init__(
            self, png: str, offset_x: int, offset_y: int, maze: list[
                list[int]], row: int = 0, col: int = 0) -> None:
        """
        initiates an instance of ghost
        """
        self.base_row = row
        self.base_col = col
        self.row = row
        self.col = col
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.lastmove = pg.time.get_ticks()
        self.last_direction = ""
        self.direction = self.chose_direction(maze)
        self.lastdeath = 0
        self.exists = True
        self.collision = False
        self.base_image = pg.transform.scale(
            pg.image.load(png), (20, 20))
        self.image = self.base_image
        self.rect = self.create()
        self.pos = self.row + self.col

    def update(self, maze: list[list[int]], prow: int,
               pcol: int, pow: bool) -> None:
        """
        will run each frame of the game, and runs different functions based
        on condition, if needs to respawn, if needs to move, chase, flee

        Arguments:
        maze -- list of hex in the maze to check walls in each cell
        prow, pcol -- position of pacman at runtime
        pow -- bool, is pacman powered up
        """
        # get current time
        time = pg.time.get_ticks()
        self.pos = self.row + self.col
        # compares current to lastmove time and decide if move, chase or flee
        if time - self.lastmove >= 500 and self.exists and abs(
                self.pos - abs(prow + pcol)) < 4 and not pow:
            self.chase(maze, prow, pcol)
            self.lastmove = time
        elif time - self.lastmove >= 500 and self.exists and abs(
                self.pos - abs(prow + pcol)) < 8 and pow:
            self.flee(maze, prow, pcol)
            self.lastmove = time
        elif time - self.lastmove >= 500 and self.exists:
            self.move(maze)
            self.lastmove = time
        # respawn timer
        if not self.exists and time - self.lastdeath >= 2500:
            self.rect = self.recreate()
            self.exists = True

    def create(self) -> pg.Rect:
        """
        creates a pygame rect with defined size and calculated x, y
        position based on the initial offset and cell sizes, in order
        to center it
        """
        x = self.offset_x + self.col * self.STEP + self.CELL_SIZE // 2
        y = self.offset_y + self.row * self.STEP + self.CELL_SIZE // 2
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        return self.rect

    def recreate(self) -> pg.Rect:
        """
        recreates a pygame rect with defined size and calculated x, y
        position based on the initial position of the ghost instance,
        used during respawn
        """
        x = self.offset_x + self.base_col * self.STEP + self.CELL_SIZE // 2
        y = self.offset_y + self.base_row * self.STEP + self.CELL_SIZE // 2
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.row = self.base_row
        self.col = self.base_col
        return self.rect

    def chose_direction(self, maze: list[list[int]]) -> str:
        """
        returns a str with the next valid direction to move ghost,
        if possible, direction will be chosen at random without
        backtracking

        Arguments:
        maze -- grid of hex valuesfor checking walls
        """
        available: list[str] = []
        # check each wall
        if not maze[self.row][self.col] & self.NORTH:
            available.append("N")
        if not maze[self.row][self.col] & self.EAST:
            available.append("E")
        if not maze[self.row][self.col] & self.SOUTH:
            available.append("S")
        if not maze[self.row][self.col] & self.WEST:
            available.append("W")
        # remove last position if possible
        opposite = {"N": "S", "S": "N", "E": "W", "W": "E"}
        if self.last_direction in available and len(available) > 1:
            available = [
                move for move in available if move[0] != opposite[
                    self.last_direction]]
        dir = random.choice(available)

        return dir

    def move(self, maze: list[list[int]]) -> None:
        """
        called during update every .5 seconds, it will change instance's
        position based on the direction chosen then chose another direction
        """
        if self.direction == "S" and not maze[self.row][self.col] & self.SOUTH:
            self.row += 1
            self.last_direction = "S"
            self.rect = self.create()
            self.direction = self.chose_direction(maze)

        elif self.direction == "N" and not maze[
                self.row][self.col] & self.NORTH:
            self.row -= 1
            self.last_direction = "N"
            self.rect = self.create()
            self.direction = self.chose_direction(maze)

        elif self.direction == "E" and not maze[
                self.row][self.col] & self.EAST:
            self.col += 1
            self.last_direction = "E"
            self.rect = self.create()
            self.direction = self.chose_direction(maze)

        elif self.direction == "W" and not maze[
                self.row][self.col] & self.WEST:
            self.col -= 1
            self.last_direction = "W"
            self.rect = self.create()
            self.direction = self.chose_direction(maze)
        else:
            self.direction = self.chose_direction(maze)
            return

    def chase(self, maze: list[list[int]], prow: int, pcol: int) -> None:
        """
        called during update every .5 seconds if pacman is near,
        it will calculate best direction to approach pacman based
        on their current positions
        """
        available: list[tuple[str, int, int]] = []
        if not maze[self.row][self.col] & self.NORTH:
            available.append(("N", self.row - 1, self.col))
        if not maze[self.row][self.col] & self.EAST:
            available.append(("E", self.row, self.col + 1))
        if not maze[self.row][self.col] & self.SOUTH:
            available.append(("S", self.row + 1, self.col))
        if not maze[self.row][self.col] & self.WEST:
            available.append(("W", self.row, self.col - 1))

        opposite = {"N": "S", "S": "N", "E": "W", "W": "E"}
        if self.last_direction and len(available) > 1:
            available = [
                move for move in available if move[0] != opposite[
                    self.last_direction]]
        # choses the minimal distance option
        bestchoice = min(
            available, key=lambda x: abs(x[1] - prow) + abs(x[2] - pcol))

        self.direction = bestchoice[0]
        self.row = bestchoice[1]
        self.col = bestchoice[2]
        self.last_direction = self.direction
        self.rect = self.create()

    def flee(self, maze: list[list[int]], prow: int, pcol: int) -> None:
        """
        called during update every .5 seconds if pacman is near,
        it will calculate best direction to escape pacman based
        on their current positions
        """
        available: list[tuple[str, int, int]] = []
        if not maze[self.row][self.col] & self.NORTH:
            available.append(("N", self.row - 1, self.col))
        if not maze[self.row][self.col] & self.EAST:
            available.append(("E", self.row, self.col + 1))
        if not maze[self.row][self.col] & self.SOUTH:
            available.append(("S", self.row + 1, self.col))
        if not maze[self.row][self.col] & self.WEST:
            available.append(("W", self.row, self.col - 1))

        opposite = {"N": "S", "S": "N", "E": "W", "W": "E"}
        if self.last_direction and len(available) > 1:
            available = [
                move for move in available if move[0] != opposite[
                    self.last_direction]]
        # choses the maximal distance option
        bestchoice = max(
            available, key=lambda x: abs(x[1] - prow) + abs(x[2] - pcol))

        self.direction = bestchoice[0]
        self.row = bestchoice[1]
        self.col = bestchoice[2]
        self.last_direction = self.direction
        self.rect = self.create()

    def die(self) -> None:
        """
        called during collision with powered-up Pac-man,
        set differents values to remove instance from screen
        """
        self.exists = False
        self.rect = pg.Rect(0, 0, 0, 0)
        self.lastdeath = pg.time.get_ticks()


class Pac():
    """
    Represents all the values of Pac-man and method to create it,
    update it, make it move
    Arguments:
    offset_x -- offset x of the grid in the screen to center it
    offset_y -- offset y of the grid in the screen to center it
    row, col -- position of the gum in grid
    base row, col -- position of the gum in grid at creation
    rect -- rectangle object with coordinates and size
    exists -- check for drawing
    power -- check if powered up
    timer -- current time for updates management
    lastdeath -- tick of lastdeath to calculate respawn
    collision -- bool indicating a collision with pac-man
    base_image, image -- used in displaying sprite png
    pos -- used to calculate position relative to pacman's
    """
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
        """
        initiates a pacman instance with base values
        """
        self.row = self.MAZE_ROWS // 2
        self.base_row = self.MAZE_ROWS // 2
        self.col = self.MAZE_COLS // 2
        self.base_col = self.MAZE_COLS // 2
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.timer = 0
        self.power = False
        self.exists = True
        self.lastdeath = 0
        self.base_image = pg.transform.scale(
            pg.image.load(pacman_path), (20, 20))
        self.image = self.base_image
        self.rect = self.create(self.row, self.col)
        self.angle = 0
        self.cheat = False

    def update(self) -> None:
        """
        will run each frame of the game, and runs different functions based
        on condition, if needs to respawn, if powered up
        """
        # get time
        time = pg.time.get_ticks()
        # removes power up after 5s
        if self.power:
            time = pg.time.get_ticks()
            if time - self.timer >= 5000:
                self.power = False
        # respawns after 2.5s
        if not self.exists and time - self.lastdeath >= 2500:
            self.rect = self.recreate()
            self.exists = True

    def power_up(self) -> None:
        """
        switch power bool and launches timer for power up duration
        """
        self.timer = pg.time.get_ticks()
        self.power = True

    def create(self, row: int, col: int) -> pg.Rect:
        """
        creates a pygame rect with defined size and calculated x, y
        position based on the initial offset and cell sizes, in order
        to center it
        """
        x = self.offset_x + col * self.STEP + self.CELL_SIZE // 2
        y = self.offset_y + row * self.STEP + self.CELL_SIZE // 2
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        return self.rect

    def recreate(self) -> pg.Rect:
        """
        recreates a pygame rect with defined size and calculated x, y
        position based on the initial position of the pacman instance,
        used during respawn
        """
        x = self.offset_x + self.base_col * self.STEP + self.CELL_SIZE // 2
        y = self.offset_y + self.base_row * self.STEP + self.CELL_SIZE // 2
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.row = self.base_row
        self.col = self.base_col
        return self.rect

    def move(self, key: int, maze: list[list[int]]) -> None:
        """
        method to move the pacman instance, it listens to keyboard inputs to
        change row and col if possible, accepts a cheat mode to alter behaviour

        Arguments:
        key -- int representing the key button pressed
        maze -- the maze grid in hex to check walls
        """
        if not self.cheat:
            if (key == pg.K_UP or key == pg.K_w) and not \
                    maze[self.row][self.col] & self.NORTH:
                self.row -= 1
                self.angle = 90
            elif (key == pg.K_DOWN or key == pg.K_s) and not \
                    maze[self.row][self.col] & self.SOUTH:
                self.row += 1
                self.angle = 270
            elif (key == pg.K_RIGHT or key == pg.K_d) and not \
                    maze[self.row][self.col] & self.EAST:
                self.col += 1
                self.angle = 0
            elif (key == pg.K_LEFT or key == pg.K_a) and not \
                    maze[self.row][self.col] & self.WEST:
                self.col -= 1
                self.angle = 180
            elif key == pg.K_c:
                self.cheat = True

        elif self.cheat:
            if (key == pg.K_UP or key == pg.K_w):
                self.row -= 1
                self.angle = 90
            elif (key == pg.K_DOWN or key == pg.K_s):
                self.row += 1
                self.angle = 270
            elif (key == pg.K_RIGHT or key == pg.K_d):
                self.col += 1
                self.angle = 0
            elif (key == pg.K_LEFT or key == pg.K_a):
                self.col -= 1
                self.angle = 180
            elif key == pg.K_c:
                self.cheat = False
        self.image = pg.transform.rotate(self.base_image, self.angle)
        self.rect = self.create(self.row, self.col)

    def die(self) -> None:
        """
        util to remove pacman from screen and start respawn timer
        """
        self.exists = False
        self.rect = pg.Rect(0, 0, 0, 0)
        self.lastdeath = pg.time.get_ticks()

    def check_mega(self, m1: pg.Rect) -> bool:
        """
        util to check if collision happened between the pacman rect
        and the megagum rect.

        Arguments:
        m1 -- megagum rect
        """
        if self.rect.colliderect(m1):
            return True
        return False

    def check_gum(self, m1: pg.Rect) -> bool:
        """
        util to check if collision happened between the pacman rect
        and the gum rect.

        Arguments:
        m1 -- gum rect
        """
        if self.rect.colliderect(m1):
            return True
        return False

    def check_collide(
            self, g1: pg.Rect) -> bool:
        """
        util to check if collision happened between the pacman rect
        and the ghost rect.

        Arguments:
        g1 -- ghost rect
        """
        if self.rect.colliderect(g1):
            return True
        return False


class Game():
    def __init__(self, config: Config) -> None:
        """
        Represents the state of the game and all the values associated to it,
        contains methods to set, reset game and update the display on screen
        Arguments:
        screen -- displays the screen using pygame
        font -- sets a font for our screen infos
        score, life, level -- base values to be displayed on screen
        allcells -- matrix of all the walls in the maze
        offsetx, offsety -- offset of the maze in the screen
        maze -- matrix of all the hex data in the maze
        """
        self.screen = pg.display.set_mode((800, 800))
        self.font = pg.font.Font(font_path, 50)
        self.score = 0
        self.life: int = config.lives
        self.level = 0
        self.time = config.level_max_time
        self.s_score = self.font.render(f"Score: {self.score}", False, "White")
        self.s_lives = self.font.render(f"Lives: {self.life}", False, "White")
        self.s_level = self.font.render(f"Level: {self.level}", False, "White")
        self.s_time = self.font.render(
            f"Time: {round(self.time, 2)}", False, "White")
        self.allcells, self.offset_x, self.offset_y, self.maze = draw_all(42)

    def reset(self, config: Config, level: int) -> None:
        """
        sets specific values during first run of the game and every restart,
        sets score to 0, level to 0, time to config value
        then creates each instance required to run and store them and creates
        the maze

        Arguments:
        config -- a parsed Config object containing configuration infos
        level -- int passed by the main program describing the current lvl
        """
        # init game state
        self.score = 0
        # self.life: int = config.lives
        self.level = 0
        self.time = config.level_max_time
        self.s_score = self.font.render(f"Score: {self.score}", False, "White")
        self.s_lives = self.font.render(f"Lives: {self.life}", False, "White")
        self.s_level = self.font.render(f"Level: {self.level}", False, "White")
        self.s_time = self.font.render(
            f"Time: {round(self.time, 2)}", False, "White")
        self.allcells, self.offset_x, self.offset_y, self.maze = draw_all(42)
        self.score = 0
        self.level = config.levels[level]['id']
        self.time = config.level_max_time

        g1_sprite = pink_path
        g2_sprite = red_path
        g3_sprite = blue_path
        g4_sprite = orange_path
        self.walls: list[tuple[pg.Rect, tuple[int, int, int]]] = []
        # create pacman
        self.pacman = Pac(self.offset_x, self.offset_y)
        # create ghosts
        self.ghost1 = Ghosts(g1_sprite, self.offset_x, self.offset_y,
                             self.maze, row=0, col=0)
        self.ghost2 = Ghosts(g2_sprite, self.offset_x, self.offset_y,
                             self.maze, row=14, col=14)
        self.ghost3 = Ghosts(g3_sprite, self.offset_x, self.offset_y,
                             self.maze, row=14, col=0)
        self.ghost4 = Ghosts(g4_sprite, self.offset_x, self.offset_y,
                             self.maze, row=0, col=14)
        self.ghosts = [self.ghost1, self.ghost2, self.ghost3, self.ghost4]
        # create megamum
        self.mega_gum1 = MegaGum(self.offset_x, self.offset_y)
        self.mega_gum2 = MegaGum(self.offset_x, self.offset_y, row=14, col=14)
        self.mega_gum3 = MegaGum(self.offset_x, self.offset_y, row=14, col=0)
        self.mega_gum4 = MegaGum(self.offset_x, self.offset_y, row=0, col=14)
        self.mgs = [self.mega_gum1, self.mega_gum2, self.mega_gum3,
                    self.mega_gum4]
        # create gums
        pos_list = open_cells(self.maze)  # list of available positions
        self.gums: list[Gum] = []
        for _ in range(config.pacgum):
            pos = random.choice(pos_list)
            g = Gum(self.offset_x, self.offset_y, row=pos[0], col=pos[1])
            pos_list.remove(pos)
            self.gums.append(g)
        # create walls with rng color
        first_wall = self.allcells[0][0]
        maze_rect = first_wall.copy()
        for cells in self.allcells:
            for wall in cells:
                maze_rect.union_ip(wall)
        for cell in self.allcells:
            for wall in cell:
                color = (random.randint(100, 255),
                         random.randint(100, 255),
                         random.randint(100, 255))
                self.walls.append((wall, color))

    def next(self, config: Config, level: int) -> None:
        """
        keep the score and life values then
        creates each instance required to run and store them and creates
        the maze using different configuration based on file

        Arguments:
        config -- a parsed Config object containing configuration infos
        level -- int passed by the main program describing the current lvl
        """
        self.allcells, self.offset_x, self.offset_y, self.maze = draw_all(0)
        self.level = config.levels[level]['id']
        self.time = config.level_max_time
        g1_sprite = pink_path
        g2_sprite = red_path
        g3_sprite = blue_path
        g4_sprite = orange_path
        # create pacman and ghosts
        self.pacman = Pac(self.offset_x, self.offset_y)
        self.ghost1 = Ghosts(g1_sprite, self.offset_x, self.offset_y,
                             self.maze, row=0, col=0)
        self.ghost2 = Ghosts(g2_sprite, self.offset_x, self.offset_y,
                             self.maze, row=14, col=14)
        self.ghost3 = Ghosts(g3_sprite, self.offset_x, self.offset_y,
                             self.maze, row=14, col=0)
        self.ghost4 = Ghosts(g4_sprite, self.offset_x, self.offset_y,
                             self.maze, row=0, col=14)
        self.ghosts = [self.ghost1, self.ghost2, self.ghost3, self.ghost4]
        self.mega_gum1 = MegaGum(self.offset_x, self.offset_y)
        self.mega_gum2 = MegaGum(self.offset_x, self.offset_y, row=14, col=14)
        self.mega_gum3 = MegaGum(self.offset_x, self.offset_y, row=14, col=0)
        self.mega_gum4 = MegaGum(self.offset_x, self.offset_y, row=0, col=14)
        self.mgs = [self.mega_gum1, self.mega_gum2, self.mega_gum3,
                    self.mega_gum4]
        pos_list = open_cells(self.maze)  # list of available positions
        for _ in range(config.levels[level]["pacgum"]):
            pos = random.choice(pos_list)
            g = Gum(self.offset_x, self.offset_y, row=pos[0], col=pos[1])
            pos_list.remove(pos)
            self.gums.append(g)
        first_wall = self.allcells[0][0]
        maze_rect = first_wall.copy()
        for cells in self.allcells:
            for wall in cells:
                maze_rect.union_ip(wall)
        for cell in self.allcells:
            for wall in cell:
                color = (random.randint(100, 255),
                         random.randint(100, 255),
                         random.randint(100, 255))
                self.walls.append((wall, color))

    def update_s(self) -> None:
        """
        runs every frame to update the text to display on screen for dynamic
        values like score, life and current level
        """
        self.s_score = self.font.render(f"Score: {self.score}", False, "White")
        self.s_lives = self.font.render(f"Lives: {self.life}", False, "White")
        self.s_level = self.font.render(f"Level: {self.level}", False, "White")
        self.s_time = self.font.render(
            f"Time: {round(self.time, 2)}", False, "White")

    def handle_event(
            self, event: pg.event.Event) -> str | None:
        """
        gets the recorded event as a parameter and returns a str
        changing the state of the game if escape key is pressed
        """
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                return "pause"
            if event.key == pg.K_l:
                self.level += 1
                return ""
            else:
                return ""
        else:
            return ""
