import pygame
from path_mgmt import font_path


class Over:
    """
    Game over screen when the game is lose and let the player chose a name
    for the highscore and give the choice to go back to menu
    """
    def __init__(self) -> None:
        """
        Init the self.text to a default value, its the player name
        """
        self.text = ""

    def draw_screen(self, screen: pygame.Surface, score: int) -> None:
        """
        Draw the game over screen

        Arguments:
        screen -- the surface where the game over screen is draw
        score -- score of the player
        """
        screen.fill("black")
        font = pygame.font.Font(font_path, 100)
        title = font.render("Game Over", False, "Yellow")
        title_rect = title.get_rect(centerx=400)
        title_rect.y = 150
        font_opt = pygame.font.Font(font_path, 80)
        opt_start = font_opt.render(f"Your score: {score}", False, "White")
        start_rect = opt_start.get_rect(centerx=400)
        start_rect.y = 250
        user_text = font_opt.render(f"Name: {self.text}", False, "White")
        user_text_rect = user_text.get_rect(centerx=400)
        user_text_rect.y = 350
        screen.blit(title, title_rect)
        screen.blit(opt_start, start_rect)
        screen.blit(user_text, user_text_rect)

    def handle_event(self, event: pygame.event.Event) -> str | None:
        """
        Handle the event when the player is on the game over screen
        Enter the username to save the score or back to main menu

        Arguments:
        event -- event of the game, the key we press
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "menu"
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                return "menu"
            elif event.unicode.isprintable() and len(self.text) < 10:
                self.text += event.unicode
        return ""
