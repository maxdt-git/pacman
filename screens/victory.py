import pygame
from path_mgmt import font_path


class Victory:
    """
    Victory screen when a level is win, ask to continu or back to main menu
    or when the game is win, let the player chose a name for the highscore
    and save it and give the choice to go back to menu
    """
    def __init__(self) -> None:
        """
        Init :
        self.text to a default value, its the player name
        self.pos, cursor position at the start of navigation
        next_colour, color of the cursor
        menu_colour, color of the options
        """
        self.text = ""
        self.pos = 0
        self.next_colour = "Pink"
        self.menu_colour = "White"

    def draw_screen(
            self, screen: pygame.Surface, score: int, level: int) -> None:
        """
        Draw the screen between every level, ask to continue or back to main
        menu, if its the last level, display the victory screen, ask to enter
        a player name or back to menu

        Arguments:
        screen -- the surface where the victory screen is draw
        """
        if level == 10:
            screen.fill("black")
            font = pygame.font.Font(font_path, 100)
            title = font.render("Victory", False, "Yellow")
            title_rect = title.get_rect(centerx=400)
            title_rect.y = 150
            font_opt = pygame.font.Font(
                font_path, 80)
            opt_start = font_opt.render(f"Your score: {score}", False, "White")
            start_rect = opt_start.get_rect(centerx=400)
            start_rect.y = 350
            user_text = font_opt.render(f"Name: {self.text}", False, "White")
            user_text_rect = user_text.get_rect(centerx=400)
            user_text_rect.y = 450
            screen.blit(title, title_rect)
            screen.blit(opt_start, start_rect)
            screen.blit(user_text, user_text_rect)
        else:
            screen.fill("black")
            font = pygame.font.Font(font_path, 100)
            title = font.render(f"Level {level} completed", False, "Yellow")
            title_rect = title.get_rect(centerx=400)
            title_rect.y = 150
            screen.blit(title, title_rect)
            font_opt = pygame.font.Font(
                font_path, 80)
            opt_next = font_opt.render("Next level", False, self.next_colour)
            opt_menu = font_opt.render("Menu", False, self.menu_colour)
            next_rect = opt_next.get_rect(centerx=400)
            next_rect.y = 350
            menu_rect = opt_menu.get_rect(centerx=400)
            menu_rect.y = 450
            screen.blit(opt_next, next_rect)
            screen.blit(opt_menu, menu_rect)

    def handle_event(self, event: pygame.event.Event,
                     level: int, screen: pygame.Surface,
                     score: int) -> str | None:
        """
        Handle the event when the player is on the victory screen
        if its the last level, enter the username to save the score
        or back to main menu

        Arguments:
        event -- event of the game, the key we press
        """
        if level == 10:
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
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN and self.pos < 1:
                    self.pos += 1
                    if self.pos == 1:
                        self.next_colour = "White"
                        self.menu_colour = "Pink"
                        self.draw_screen(screen, score, level)

                if event.key == pygame.K_UP and self.pos > 0:
                    self.pos -= 1
                    if self.pos == 0:
                        self.menu_colour = "White"
                        self.next_colour = "Pink"
                        self.draw_screen(screen, score, level)

                if event.key == pygame.K_RETURN:
                    if self.pos == 0:
                        return "next"
                    elif self.pos == 1:
                        return "menu"
        return ""
