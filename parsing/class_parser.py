from typing import Any


class Config():
    """
    Set all the value we get from the config files

    Attributes:
    pacgum: number of pacgum
    point_per_pacgum: points we get when eating a pacgum
    point_per_super_pacgum: points we get when eating a super pacgum
    point_per_ghost: points we get when eating a ghost
    seed: which maze iit will generate
    level_max_time: time for a level
    lives: how many lives for the game
    highscore_filename: name of the highscore file generated
    levels: number of levels, with particularity for each level
    """
    def __init__(self, config: dict[str, Any] | None) -> None:
        """
        Config class, init with the config data

        Arguments:
        config -- config data from the config file
        """
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
    """
    Default config if a data doesnt exist in the config file or
    if an invalid value is set

    Attributes:
    pacgum: number of pacgum
    point_per_pacgum: points we get when eating a pacgum
    point_per_super_pacgum: points we get when eating a super pacgum
    point_per_ghost: points we get when eating a ghost
    seed: which maze iit will generate
    level_max_time: time for a level
    lives: how many lives for the game
    highscore_filename: name of the highscore file generated
    levels: number of levels, with particularity for each level
    """
    def __init__(self) -> None:
        """
        Init all the atributes we need to run the game
        """
        self.pacgum = 42
        self.points_per_pacgum = 10
        self.points_per_super_pacgum = 50
        self.points_per_ghost = 200
        self.seed = 42
        self.level_max_time = 90
        self.lives = 3
        self.highscore_filename = "highscore.json"
        self.levels = [
            {
                "id": 1,
                "height": 15,
                "width": 15,
                "pacgum": 1
            },
            {
                "id": 2,
                "height": 15,
                "width": 15,
                "pacgum": 5
            },
            {
                "id": 3,
                "height": 15,
                "width": 15,
                "pacgum": 10
            },
            {
                "id": 4,
                "height": 15,
                "width": 15,
                "pacgum": 15
            },
            {
                "id": 5,
                "height": 15,
                "width": 15,
                "pacgum": 20
            },
            {
                "id": 6,
                "height": 15,
                "width": 15,
                "pacgum": 30
            },
            {
                "id": 7,
                "height": 15,
                "width": 15,
                "pacgum": 40
            },
            {
                "id": 8,
                "height": 15,
                "width": 15,
                "pacgum": 50
            },
            {
                "id": 9,
                "height": 15,
                "width": 15,
                "pacgum": 60
            },
            {
                "id": 10,
                "height": 15,
                "width": 15,
                "pacgum": 80
            }
            ]
