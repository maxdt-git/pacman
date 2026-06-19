import pygame


class Pause():
    def __init__(self) -> None:
        self.start_colour = "Pink"
        self.score_colour = "White"
        self.tuto_colour = "White"
        self.exit_colour = "White"
        self.pos = 0

    def draw_screen(self, screen: pygame.Surface) -> None:
        screen.fill("black")
        font = pygame.font.Font("fonts/Pixeltype.ttf", 100)
        title = font.render("Pause", False, "Yellow")
        title_rect = title.get_rect(centerx=400)
        title_rect.y = 150
        font_opt = pygame.font.Font("fonts/Pixeltype.ttf", 80)
        opt_resume = font_opt.render("Resume game", False, self.start_colour)
        opt_exit = font_opt.render("Return to the main menu",
                                   False, self.score_colour)
        start_rect = opt_resume.get_rect(centerx=400)
        start_rect.y = 300
        exit_rect = opt_exit.get_rect(centerx=400)
        exit_rect.y = 400
        screen.blit(title, title_rect)
        screen.blit(opt_resume, start_rect)
        screen.blit(opt_exit, exit_rect)

    def handle_event(
            self, event: pygame.event.Event, screen: pygame.Surface
            ) -> str | None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN and self.pos < 1:
                self.pos += 1
                if self.pos == 1:
                    self.start_colour = "White"
                    self.score_colour = "Pink"
                    self.draw_screen(screen)
                elif self.pos == 2:
                    self.score_colour = "White"
                    self.tuto_colour = "Pink"
                    self.draw_screen(screen)

            if event.key == pygame.K_UP and self.pos > 0:
                self.pos -= 1
                if self.pos == 1:
                    self.tuto_colour = "White"
                    self.score_colour = "Pink"
                    self.draw_screen(screen)
                elif self.pos == 0:
                    self.score_colour = "White"
                    self.start_colour = "Pink"
                    self.draw_screen(screen)

            if event.key == pygame.K_RETURN:
                if self.pos == 0:
                    return "game"
                elif self.pos == 1:
                    return "menu"
            else:
                return ""
        else:
            return ""
