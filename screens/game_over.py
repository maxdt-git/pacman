import pygame


class Over:
    def __init__(self):
        self.text = ""

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
        user_text = font_opt.render("Name: " + self.text, False, "White")
        user_text_rect = user_text.get_rect(centerx=400)
        user_text_rect.y = 350
        screen.blit(title, title_rect)
        screen.blit(opt_start, start_rect)
        screen.blit(user_text, user_text_rect)

    def handle_event(self, event: pygame.event.Event) -> str | None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "menu"
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                return "menu"
            elif event.unicode.isprintable():
                self.text += event.unicode
