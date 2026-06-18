import pygame
from sys import exit, argv
from random import randint
from generator import Game, Pac, Ghosts, Run
from screens import Menu, Score, Tuto, Pause, Over
from parsing import check_config, extract_dict, Config


def main():

    pygame.init()
    conf = extract_dict(argv[1])
    parsed = check_config(conf)
    config = Config(parsed)

    game = Game()
    menu = Menu()
    score = Score()
    tuto = Tuto()
    pause = Pause()
    run = Run()
    over = Over()
    clock = pygame.time.Clock()
    state = "menu"

    walls: list[tuple[pygame.Rect, tuple[int, int, int]]] = []

    pacman = Pac(game.offset_x, game.offset_y)
    ghost1 = Ghosts(game.offset_x, game.offset_y, game.maze)
    ghost2 = Ghosts(game.offset_x, game.offset_y, game.maze, row=14, col=14)
    ghost3 = Ghosts(game.offset_x, game.offset_y, game.maze, row=14, col=0)
    ghost4 = Ghosts(game.offset_x, game.offset_y, game.maze, row=0, col=14)

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
            if state == "game":
                game.screen.fill("black")  # erase screen
                game.screen.blit(game.text_surface, (50, 750))  # draw score
                for wall, color in walls:  # draw maze
                    if wall.width == wall.height:
                        pygame.draw.rect(
                            game.screen, pygame.Color(245, 223, 52, 10), wall)
                    else:
                        pygame.draw.rect(
                            game.screen, pygame.Color(color), wall)
                pygame.draw.rect(game.screen, "Red", pacman.rect)  # draw pac
                pygame.draw.rect(game.screen, "Blue", ghost1.rect)  # draw gh

                if event.type == pygame.KEYDOWN:
                    pacman.move(event.key, game.maze)
                    game.screen.fill("black")
                    game.screen.blit(game.text_surface, (50, 750))
                    for wall, color in walls:
                        if wall.width == wall.height:
                            pygame.draw.rect(
                                game.screen, pygame.Color(
                                    245, 223, 52, 10), wall)
                        else:
                            pygame.draw.rect(
                                game.screen, pygame.Color(color), wall)
                    pygame.draw.rect(game.screen, "Red", pacman.rect)
            if state == "over":
                run.life = 3
                select = over.handle_event(event)
                if select == "menu":
                    state = "menu"

        if state == "menu":
            menu.draw_screen(game.screen)
        if state == "score":
            game.screen.fill("black")
            score.draw_screen(game.screen)
        if state == "tuto":
            game.screen.fill("black")
            tuto.draw_screen(game.screen)
        if state == "game":
            if run.life <= 0:
                state = "over"
            if pacman.check_collide(
                    ghost1.rect, ghost2.rect, ghost3.rect, ghost4.rect):
                run.life -= 1
            ghost1.update(game.maze)
            ghost2.update(game.maze)
            ghost3.update(game.maze)
            ghost4.update(game.maze)
            game.screen.fill("black")  # erase screen
            game.screen.blit(game.text_surface, (50, 750))  # draw score
            for wall, color in walls:  # draw maze
                if wall.width == wall.height:
                    pygame.draw.rect(
                        game.screen, pygame.Color(245, 223, 52, 10), wall)
                else:
                    pygame.draw.rect(
                        game.screen, pygame.Color(color), wall)
            pygame.draw.rect(game.screen, "Red", pacman.rect)  # draw pac
            pygame.draw.rect(game.screen, "Blue", ghost1.rect)  # draw gh
            pygame.draw.rect(game.screen, "Green", ghost2.rect)  # draw gh
            pygame.draw.rect(game.screen, "Pink", ghost3.rect)  # draw gh
            pygame.draw.rect(game.screen, "Purple", ghost4.rect)  # draw gh
        if state == "over":
            over.draw_screen(game.screen)
        clock.tick(60)
        pygame.display.update()


if __name__ == "__main__":
    main()
