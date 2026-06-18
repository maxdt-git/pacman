import pygame


class Over:
    def draw_screen(self, screen: pygame.Surface) -> None:
        screen.fill("black")
        font = pygame.font.Font("fonts/Pixeltype.ttf", 100)
        title = font.render("Game Over", False, "Yellow")
        title_rect = title.get_rect(centerx=400)
        title_rect.y = 150
        font_opt = pygame.font.Font("fonts/Pixeltype.ttf", 80)
        opt_start = font_opt.render("Your score: 1200", False, "White")
        start_rect = opt_start.get_rect(centerx=400)
        start_rect.y = 250
        screen.blit(title, title_rect)
        screen.blit(opt_start, start_rect)

    def handle_event(self, event: pygame.event.Event) -> str:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "menu"
            else:
                return ""
        else:
            return ""
