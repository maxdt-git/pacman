from typing import Any


class Config():
    def __init__(self, config: dict[str, Any] | None) -> None:
        if not config:
            return None
        self.pacgum = config['pacgum']
        self.points_per_pacgum = config['points_per_pacgum']
        self.points_per_super_pacgum = config['points_per_super_pacgum']
        self.points_per_ghost = config['points_per_ghost']
        self.seed = config['seed']
        self.level_max_time = config['level_max_time']
        self.lives = config['lives']
        self.highscore_filename = config['highscore_filename']
        self.levels = config['levels']


class DefaultConfig():
    def __init__(self) -> None:
        self.pacgum = 42
        self.points_per_pacgum = 10
        self.points_per_super_pacgum = 50
        self.points_per_ghost = 200
        self.seed = 42
        self.level_max_time = 90
        self.lives = 3
        self.highscore_filename = "hs.json"
        self.levels = [{
            "id": 1, "height": 15, "width": 15}, {
                "id": 2, "height": 15, "width": 15}, {
                    "id": 3, "height": 15, "width": 15}, {
                        "id": 4, "height": 15, "width": 15}, {
                            "id": 5, "height": 15, "width": 15}, {
                                "id": 6, "height": 15, "width": 15}, {
                                    "id": 7, "height": 15, "width": 15}, {
                                        "id": 8, "height": 15, "width": 15}, {
                                            "id": 9, "height": 15,
                                            "width": 15}, {
                                                "id": 10, "height": 15,
                                                "width": 15}]
