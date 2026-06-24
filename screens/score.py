import pygame
import json
from parsing import Config
from typing import Any
from path_mgmt import font_path


def extract_score(jsonfile: str) -> Any | None:
    """
    Open the jsonfile where the highscores are saved and transforms
    the data so they can be used

    Arguments:
    jsonfile -- name of the config file
    """
    try:
        with open(jsonfile, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return None
    except Exception as e:
        print(e)
        return None


class Score:
    """
    Create the highscore screen where the top 10 best scores
    are saved and draw it
    """
    def draw_screen(self, screen: pygame.Surface, config: Config) -> None:
        """
        Draw the score screen with username: score

        Arguments:
        screen -- the surface where the highscore screen is draw
        score -- score of the player
        """
        screen.fill("black")
        font = pygame.font.Font(font_path, 100)
        title = font.render("Highscores", False, "Yellow")
        title_rect = title.get_rect(centerx=400)
        title_rect.y = 150
        font_opt = pygame.font.Font(font_path, 80)
        scores = extract_score(config.highscore_filename)
        if not scores:
            no_score = font.render("No score", False, "White")
            no_score_rect = no_score.get_rect(centerx=400)
            no_score_rect.y = 250
            screen.blit(no_score, no_score_rect)
            return None
        sort_scores = dict(sorted(scores.items(),
                                  key=lambda item: item[1], reverse=True))
        screen.blit(title, title_rect)
        y = 250
        for name in sort_scores:
            opt_start = font_opt.render(
                f"{name} : {sort_scores[name]}", False, "White")
            start_rect = opt_start.get_rect(centerx=400)
            start_rect.y = y
            screen.blit(opt_start, start_rect)
            y += 50

    def handle_event(self, event: pygame.event.Event) -> str:
        """
        Handle the event when the player is on the score screen,
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
