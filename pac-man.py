import pygame
import json
from sys import exit, argv
from random import randint
from generator import Game
from screens import Menu, Score, Tuto, Pause, Over, Victory
from parsing import check_config, extract_config, Config
from path_mgmt import vul_path


def main() -> None:

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
    victory = Victory()
    clock = pygame.time.Clock()
    state = "menu"
    curlvl = 0
    vpng = vul_path
    game.reset(config, curlvl)
    pygame.display.set_caption("Pac-Man")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if state == "menu":
                select = menu.handle_event(event, game.screen)
                if select == "game":
                    curlvl = 0
                    game.reset(config, curlvl)
                    game.life = config.lives
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
                if event.type == pygame.KEYDOWN and game.pacman.exists:
                    game.pacman.move(event.key, game.maze)
                if game.time == 0:
                    state = "over"
            if state == "over":
                game.life = 3
                game.time = config.level_max_time
                game.level = config.levels[0]['id']
                select = over.handle_event(event)
                if select == "menu":
                    scores_vic: dict[str, int] = {}
                    if over.text:
                        try:
                            with open(config.highscore_filename, "r") as f:
                                scores_vic = json.load(f)
                        except Exception:
                            scores_vic = {}
                        scores_vic[over.text] = game.score
                        scores_vic = dict(sorted(scores_vic.items(),
                                                 key=lambda item: item[1],
                                                 reverse=True)[:10])
                        with open(config.highscore_filename, "w") as f:
                            json.dump(scores_vic, f)
                    over.text = ""
                    state = "menu"
            if state == "victory":
                select = victory.handle_event(event, game.level, game.screen,
                                              game.score)
                if select == "menu" and game.level == 10:
                    scores: dict[str, int] = {}
                    if victory.text:
                        try:
                            with open(config.highscore_filename, "r") as f:
                                scores = json.load(f)
                        except Exception:
                            scores = {}
                        scores[victory.text] = game.score
                        scores = dict(sorted(scores.items(),
                                             key=lambda item: item[1],
                                             reverse=True)[:10])
                        with open(config.highscore_filename, "w") as f:
                            json.dump(scores, f)
                    victory.text = ""
                    state = "menu"
                elif select == "menu":
                    state = "menu"
                elif select == "next":
                    curlvl += 1
                    game.walls = []
                    game.gums = []
                    game.next(config, curlvl)
                    state = "game"
                    continue

        if state == "menu":
            menu.draw_screen(game.screen)
        if state == "score":
            game.screen.fill("black")
            score.draw_screen(game.screen, config)
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
            if not game.pacman.cheat:
                for gh in game.ghosts:
                    if game.pacman.check_collide(gh.rect):
                        if game.pacman.power:
                            gh.die()
                            game.score += config.points_per_ghost
                        elif not gh.collision:
                            gh.collision = True
                            game.pacman.die()
                            game.life -= 1
                            break
                    else:
                        gh.collision = False
                #
                # check game.pacman eats megagum
                #
                for mg in game.mgs:
                    if game.pacman.check_mega(mg.rect):
                        game.pacman.power_up()
                        mg.exists = False
                        game.mgs.remove(mg)
                        game.score += config.points_per_super_pacgum
                #
                # check game.pacman eats gum
                #
            for gum in game.gums:
                if game.pacman.check_mega(gum.rect):
                    gum.exists = False
                    game.gums.remove(gum)
                    game.score += config.points_per_pacgum
            #
            # update for pac and ghost to move them or remove power up
            #
            game.pacman.update()
            for gh in game.ghosts:
                gh.update(game.maze, game.pacman.row, game.pacman.col,
                          game.pacman.power)
            game.update_s()
            #
            # draw screen
            #
            game.screen.fill("black")  # erase screen
            game.screen.blit(game.s_score, (50, 750))  # draw score
            game.screen.blit(game.s_lives, (50, 25))  # draw lives
            game.screen.blit(game.s_level, (600, 25))  # draw level
            game.screen.blit(game.s_time, (600, 750))  # draw time
            if not game.pacman.power:
                for wall, color in game.walls:  # draw maze
                    if wall.width == wall.height:
                        pygame.draw.rect(
                            game.screen, pygame.Color(245, 223, 52, 10), wall)
                    else:
                        pygame.draw.rect(
                            game.screen, pygame.Color(color), wall)
            else:
                for cell in game.allcells:
                    for wall in cell:
                        pygame.draw.rect(
                            game.screen, pygame.Color((randint(100, 255),
                                                       randint(100, 255),
                                                       randint(100, 255))),
                            wall)
            # draw rect
            #
            # game.pacman
            if game.pacman.exists:
                game.screen.blit(game.pacman.image, game.pacman.rect)
            #  megagum
            for mg in game.mgs:
                if mg.exists:
                    pygame.draw.circle(
                        game.screen, "White", mg.rect.center, 6)
            #  gums
            for g in game.gums:
                pygame.draw.circle(game.screen, "White", g.rect.center, 4)
            # ghosts
            for gh in game.ghosts:
                if gh.exists and not game.pacman.power:
                    game.screen.blit(gh.image, gh.rect)
                elif gh.exists and game.pacman.power:
                    game.screen.blit(pygame.transform.scale(
                        pygame.image.load(vpng), (20, 20)), gh.rect)

            game.time -= 0.01666
            if game.time < 0:
                state = "over"
            if len(game.gums) == 0:
                state = "victory"

        if state == "over":
            over.draw_screen(game.screen, game.score)
        if state == "victory":
            victory.draw_screen(game.screen, game.score, game.level)
        clock.tick(60)
        pygame.display.update()


if __name__ == "__main__":
    main()
