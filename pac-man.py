import pygame
from sys import exit
from random import randint
from screens import Menu
from generator import Pacman, Ghosts, Game
from screens import Menu, Score, Tuto


def main():

    pygame.init()

    game = Game()
    clock = pygame.time.Clock()

    walls: list[tuple[pygame.Rect, tuple[int, int, int]]] = []

    pacman = Pacman(800, 800)
    g1 = Ghosts(700, 672)
    g2 = Ghosts(88, 672)
    g3 = Ghosts(700, 50)
    g4 = Ghosts(88, 50)
    menu = Menu()
    score = Score()
    tuto = Tuto()
    for cell in game.allcells:
        for wall in cell:
            color = (randint(100, 255),
                     randint(100, 255),
                     randint(100, 255))
            walls.append((wall, color))
    state = "menu"
    speed = 0.100

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if state == "menu":
                menu.draw_screen(game.screen)
            # else:
            #     game.screen.fill((0, 0, 0))
                # game.screen.blit(game.text_surface, (50, 750))
                menu.draw_screen(game.screen)
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
                game.screen.fill("black")
                score.draw_screen(game.screen)
                select = score.handle_event(event)
                if select == "menu":
                    state = "menu"
            if state == "tuto":
                game.screen.fill("black")
                tuto.draw_screen(game.screen)
                select = tuto.handle_event(event)
                if select == "menu":
                    state = "menu"
            if state == "exit":
                pygame.quit()
                exit()
            if state == "game":
                game.screen.fill("black")
                game.screen.blit(game.text_surface, (50, 750))
                for wall, color in walls:
                    if wall.width == wall.height:
                        pygame.draw.rect(
                            game.screen, pygame.Color(245, 223, 52, 10), wall)
                    else:
                        pygame.draw.rect(
                            game.screen, pygame.Color(color), wall)
                        keys = pygame.key.get_pressed()

                        if keys[pygame.K_LEFT] and pacman.rect.left > 0:
                            pacman.pos_x -= speed
                            pacman.angle = 180

                        if keys[pygame.K_RIGHT] and pacman.rect.left < 800:
                            pacman.pos_x += speed
                            pacman.angle = 0

                        if keys[pygame.K_UP] and pacman.rect.top > 0:
                            pacman.pos_y -= speed
                            pacman.angle = 90

                        if keys[pygame.K_DOWN] and pacman.rect.top < 800:
                            pacman.pos_y += speed
                            pacman.angle = 270

                        pacman.rect.topleft = (int(pacman.pos_x), int(
                            pacman.pos_y))
                        pacman.rot = pygame.transform.rotate(
                            pacman.image, pacman.angle)
                        game.screen.blit(pacman.rot, pacman.rect)

                        game.screen.blit(g1.image, (g1.pos_x, g1.pos_y))
                        game.screen.blit(g2.image, (g2.pos_x, g2.pos_y))
                        game.screen.blit(g3.image, (g3.pos_x, g3.pos_y))
                        game.screen.blit(g4.image, (g4.pos_x, g4.pos_y))

        clock.tick(60)
        pygame.display.update()


if __name__ == "__main__":
    main()
