import pygame
from path_mgmt import font_path


class Tuto:
    """
    Create the tuto screen where the tutorial is
    """
    def draw_screen(self, screen: pygame.Surface) -> None:
        """
        Draw the tuto screen where are the indications
        to play the game

        screen -- the surface where the tutorial screen is draw
        """
        screen.fill("black")
        font = pygame.font.Font(font_path, 100)
        title = font.render("How-To-Play", False, "Yellow")
        title_rect = title.get_rect(centerx=400)
        title_rect.y = 150
        font_opt = pygame.font.Font(font_path, 70)
        opt_1 = font_opt.render(
            "- Use WASD or Arrow keys to move -", False, "White")
        opt_2 = font_opt.render(
            "- Press Space to pause game -", False, "White")
        start_rect = opt_1.get_rect(centerx=400)
        start_rect.y = 250
        sp_rect = opt_2.get_rect(centerx=400)
        sp_rect.y = 350
        screen.blit(title, title_rect)
        screen.blit(opt_1, start_rect)
        screen.blit(opt_2, sp_rect)

    def handle_event(self, event: pygame.event.Event) -> str:
        """
        Handle the event when the player is on the tuto screen,
        press escape to go back to main menu

        Arguments:
        event -- event of the game, the key we press
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "menu"
            else:
                return ""
        else:
            return ""
