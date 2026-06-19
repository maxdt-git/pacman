import pygame
import json


def extract_score(jsonfile: str) -> dict[str, int] | None:
    try:
        with open(jsonfile, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return None
    except Exception as e:
        print(e)
        return None


class Score:
    def draw_screen(self, screen: pygame.Surface) -> None:
        screen.fill("black")
        font = pygame.font.Font("fonts/Pixeltype.ttf", 100)
        title = font.render("Highscores", False, "Yellow")
        title_rect = title.get_rect(centerx=400)
        title_rect.y = 150
        font_opt = pygame.font.Font("fonts/Pixeltype.ttf", 80)
        scores = extract_score("hs.json")
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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "menu"
            else:
                return ""
        else:
            return ""
