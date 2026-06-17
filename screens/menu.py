import pygame


class Menu:
    def __init__(self) -> None:
        self.start_colour = "Pink"
        self.score_colour = "White"
        self.tuto_colour = "White"
        self.exit_colour = "White"
        self.pos = 0

    def draw_screen(self, screen: pygame.Surface) -> None:
        screen.fill("black")
        font = pygame.font.Font("fonts/Pixeltype.ttf", 100)
        title = font.render("Pac-Man", False, "Yellow")
        title_rect = title.get_rect(centerx=400)
        title_rect.y = 150
        font_opt = pygame.font.Font("fonts/Pixeltype.ttf", 80)
        opt_start = font_opt.render("Start", False, self.start_colour)
        opt_score = font_opt.render("Highscores", False, self.score_colour)
        opt_tuto = font_opt.render("How-to-play", False, self.tuto_colour)
        opt_exit = font_opt.render("Exit", False, self.exit_colour)
        start_rect = opt_start.get_rect(centerx=400)
        start_rect.y = 250
        score_rect = opt_score.get_rect(centerx=400)
        score_rect.y = 350
        tuto_rect = opt_tuto.get_rect(centerx=400)
        tuto_rect.y = 450
        exit_rect = opt_exit.get_rect(centerx=400)
        exit_rect.y = 550
        screen.blit(title, title_rect)
        screen.blit(opt_start, start_rect)
        screen.blit(opt_score, score_rect)
        screen.blit(opt_tuto, tuto_rect)
        screen.blit(opt_exit, exit_rect)

    def handle_event(
            self, event: pygame.event.Event, screen: pygame.Surface
            ) -> str | None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN and self.pos < 3:
                self.pos += 1
                if self.pos == 1:
                    self.start_colour = "White"
                    self.score_colour = "Pink"
                    self.draw_screen(screen)
                elif self.pos == 2:
                    self.score_colour = "White"
                    self.tuto_colour = "Pink"
                    self.draw_screen(screen)
                elif self.pos == 3:
                    self.tuto_colour = "White"
                    self.exit_colour = "Pink"
                    self.draw_screen(screen)

            if event.key == pygame.K_UP and self.pos > 0:
                self.pos -= 1
                if self.pos == 1:
                    self.tuto_colour = "White"
                    self.score_colour = "Pink"
                    self.draw_screen(screen)
                elif self.pos == 2:
                    self.exit_colour = "White"
                    self.tuto_colour = "Pink"
                    self.draw_screen(screen)
                elif self.pos == 0:
                    self.score_colour = "White"
                    self.start_colour = "Pink"
                    self.draw_screen(screen)

            if event.key == pygame.K_RETURN:
                if self.pos == 0:
                    return "game"
                elif self.pos == 1:
                    return "score"
                elif self.pos == 2:
                    return "tuto"
                elif self.pos == 3:
                    return "exit"
            else:
                return ""
        else:
            return ""
