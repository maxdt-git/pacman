import pygame
import json
from sys import exit, argv
from random import randint
from generator import Game, Pac, Ghosts, MegaGum
from screens import Menu, Score, Tuto, Pause, Over
from parsing import check_config, extract_config, Config


def main():

    pygame.init()
    if len(argv) != 2:
        print("Insert config file")
        return
    conf = extract_config(argv[1])
    parsed = check_config(conf)
    config = Config(parsed)

    game = Game(config)
    menu = Menu()
    score = Score()
    tuto = Tuto()
    pause = Pause()
    over = Over()
    clock = pygame.time.Clock()
    state = "menu"

    walls: list[tuple[pygame.Rect, tuple[int, int, int]]] = []

    pacman = Pac(game.offset_x, game.offset_y)
    ghost1 = Ghosts(game.offset_x, game.offset_y, game.maze)
    ghost2 = Ghosts(game.offset_x, game.offset_y, game.maze, row=14, col=14)
    ghost3 = Ghosts(game.offset_x, game.offset_y, game.maze, row=14, col=0)
    ghost4 = Ghosts(game.offset_x, game.offset_y, game.maze, row=0, col=14)

    mega_gum1 = MegaGum(game.offset_x, game.offset_y)
    mega_gum2 = MegaGum(game.offset_x, game.offset_y, row=14, col=14)
    mega_gum3 = MegaGum(game.offset_x, game.offset_y, row=14, col=0)
    mega_gum4 = MegaGum(game.offset_x, game.offset_y, row=0, col=14)

    first_wall = game.allcells[0][0]
    maze_rect = first_wall.copy()
    for cells in game.allcells:
        for wall in cells:
            maze_rect.union_ip(wall)
    for cell in game.allcells:
        for wall in cell:
            color = (randint(100, 255),
                     randint(100, 255),
                     randint(100, 255))
            walls.append((wall, color))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if state == "menu":
                select = menu.handle_event(event, game.screen)
                if select == "game":
                    state = "game"
                if select == "score":
                    state = "score"
                if select == "tuto":
                    state = "tuto"
                if select == "exit":
                    state = "exit"
                if select == "pause":
                    state = "pause"
            if state == "score":
                select = score.handle_event(event)
                if select == "menu":
                    state = "menu"
            if state == "tuto":
                select = tuto.handle_event(event)
                if select == "menu":
                    state = "menu"
            if state == "exit":
                pygame.quit()
                exit()
            if state == "pause":
                select = pause.handle_event(event, game.screen)
                if select == "game":
                    state = "game"
                if select == "menu":
                    state = "menu"
            if state == "game":
                select = game.handle_event(event)
                if select == "pause":
                    state = "pause"
                if event.type == pygame.KEYDOWN:
                    pacman.move(event.key, game.maze)
                if game.time == 0:
                    state = "over"
            if state == "over":
                game.life = 3
                game.time = config.level_max_time
                game.level = config.levels[0]['id']
                select = over.handle_event(event)
                if select == "menu":
                    if over.text:
                        try:
                            with open("hs.json", "r") as f:
                                scores = json.load(f)
                        except Exception:
                            scores = {}
                        scores[over.text] = game.score
                        with open("hs.json", "w") as f:
                            json.dump(scores, f)
                    over.text = ""
                    state = "menu"

        if state == "menu":
            menu.draw_screen(game.screen)
        if state == "score":
            game.screen.fill("black")
            score.draw_screen(game.screen)
        if state == "tuto":
            game.screen.fill("black")
            tuto.draw_screen(game.screen)
        if state == "pause":
            game.screen.fill("black")
            pause.draw_screen(game.screen)
        if state == "game":
            if game.life <= 0:
                state = "over"
            #
            # check pacman collides ghost
            #
            if pacman.check_collide(ghost1.rect):
                if pacman.power:
                    ghost1.exists = False
                    ghost1.lastdeath = pygame.time.get_ticks()
                elif not ghost1.collision:
                    pacman.rect = pygame.Rect(0, 0, 0, 0)
                    pacman.exists = False
                    pacman.lastdeath = pygame.time.get_ticks()
                    ghost1.collision = True
                    game.life -= 1

            else:
                ghost1.collision = False

            if pacman.check_collide(ghost2.rect):
                if pacman.power:
                    ghost2.exists = False
                    ghost2.lastdeath = pygame.time.get_ticks()
                elif not ghost2.collision:
                    pacman.rect = pygame.Rect(0, 0, 0, 0)
                    pacman.exists = False
                    pacman.lastdeath = pygame.time.get_ticks()
                    ghost2.collision = True
                    game.life -= 1

            else:
                ghost2.collision = False

            if pacman.check_collide(ghost3.rect):
                if pacman.power:
                    ghost3.exists = False
                    ghost3.lastdeath = pygame.time.get_ticks()
                elif not ghost3.collision:
                    pacman.rect = pygame.Rect(0, 0, 0, 0)
                    pacman.exists = False
                    pacman.lastdeath = pygame.time.get_ticks()
                    ghost3.collision = True
                    game.life -= 1

            else:
                ghost3.collision = False

            if pacman.check_collide(ghost4.rect):
                if pacman.power:
                    ghost4.exists = False
                    ghost4.lastdeath = pygame.time.get_ticks()
                elif not ghost4.collision:
                    pacman.rect = pygame.Rect(0, 0, 0, 0)
                    pacman.exists = False
                    pacman.lastdeath = pygame.time.get_ticks()
                    ghost4.collision = True
                    game.life -= 1

            else:
                ghost4.collision = False
            #
            # check pacman eats megagum
            #
            if pacman.check_mega(mega_gum1.rect):
                pacman.power_up()
                mega_gum1.exists = False
            if pacman.check_mega(mega_gum2.rect):
                pacman.power_up()
                mega_gum2.exists = False
            if pacman.check_mega(mega_gum3.rect):
                pacman.power_up()
                mega_gum3.exists = False
            if pacman.check_mega(mega_gum4.rect):
                pacman.power_up()
                mega_gum4.exists = False
            #
            # update for pac and ghost to move them or remove power up
            #
            pacman.update()
            ghost1.update(game.maze)
            ghost2.update(game.maze)
            ghost3.update(game.maze)
            ghost4.update(game.maze)
            #
            # draw screen
            #
            game.screen.fill("black")  # erase screen
            game.update_s()
            game.screen.blit(game.s_score, (50, 750))  # draw score
            game.screen.blit(game.s_lives, (50, 25))
            game.screen.blit(game.s_level, (600, 25))
            game.screen.blit(game.s_time, (600, 750))
            for wall, color in walls:  # draw maze
                if wall.width == wall.height:
                    pygame.draw.rect(
                        game.screen, pygame.Color(245, 223, 52, 10), wall)
                else:
                    pygame.draw.rect(
                        game.screen, pygame.Color(color), wall)
            #
            # draw rect
            #
            # pacman
            if pacman.exists:
                if pacman.power:
                    pygame.draw.rect(game.screen, "Yellow", pacman.rect)
                else:
                    pygame.draw.rect(game.screen, "Red", pacman.rect)  # drawp
            # ghosts
            if ghost1.exists:
                pygame.draw.rect(game.screen, "Blue", ghost1.rect)  # draw gh
            if ghost2.exists:
                pygame.draw.rect(game.screen, "Green", ghost2.rect)  # draw gh
            if ghost3.exists:
                pygame.draw.rect(game.screen, "Pink", ghost3.rect)  # draw gh
            if ghost4.exists:
                pygame.draw.rect(game.screen, "Purple", ghost4.rect)  # draw gh
            #  megagum
            if mega_gum1.exists:
                pygame.draw.circle(
                    game.screen, "White", mega_gum1.rect.center, 6)
            if mega_gum2.exists:
                pygame.draw.circle(
                    game.screen, "White", mega_gum2.rect.center, 6)
            if mega_gum3.exists:
                pygame.draw.circle(
                    game.screen, "White", mega_gum3.rect.center, 6)
            if mega_gum4.exists:
                pygame.draw.circle(
                    game.screen, "White", mega_gum4.rect.center, 6)
            game.time -= 0.017
            if game.time < 0:
                state = "over"
        if state == "over":
            over.draw_screen(game.screen)
        clock.tick(60)
        pygame.display.update()


if __name__ == "__main__":
    main()
