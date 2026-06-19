import json
from typing import Any
from parsing import DefaultConfig


def extract_config(jsonfile: str) -> dict[str, Any] | None:
    try:
        with open(jsonfile, "r") as file:
            return json.load(file)
    except Exception as e:
        print(e)
        return None


def check_config(config: dict[str, Any] | None) -> dict[str, Any] | None:

    mandatory_keys = [
        "pacgum", "points_per_pacgum", "points_per_super_pacgum",
        "points_per_ghost", "seed", "level_max_time", "lives",
        "highscore_filename", "levels"]

    defaut = DefaultConfig()

    if not config:
        return None
    for key in mandatory_keys:
        if key not in config:
            if key == 'pacgum':
                config['pacgum'] = defaut.pacgum
            if key == 'points_per_pacgum':
                config['points_per_pacgum'] = defaut.points_per_pacgum
            if key == 'points_per_super_pacgum':
                config['points_per_super_pacgum'] = \
                    defaut.points_per_super_pacgum
            if key == 'points_per_ghost':
                config['points_per_ghost'] = defaut.points_per_ghost
            if key == 'seed':
                config['seed'] = defaut.seed
            if key == 'level_max_time':
                config['level_max_time'] = defaut.level_max_time
            if key == 'lives':
                config['lives'] = defaut.lives
            if key == 'highscore_filename':
                config['highscore_filename'] = defaut.highscore_filename
            if key == 'levels':
                config['levels'] = defaut.levels

            print(f"{key} missing, set to default value {config[key]}")

    for key in config:
        if key == 'pacgum':
            if not isinstance(config['pacgum'], int):
                config['pacgum'] = defaut.pacgum
        if key == 'points_per_pacgum':
            if not isinstance(config['points_per_pacgum'], int):
                config['points_per_pacgum'] = defaut.points_per_pacgum
        if key == 'points_per_super_pacgum':
            if not isinstance(config['points_per_super_pacgum'], int):
                config['points_per_super_pacgum'] = \
                    defaut.points_per_super_pacgum
        if key == 'points_per_ghost':
            if not isinstance(config['points_per_ghost'], int):
                config['points_per_ghost'] = defaut.points_per_ghost
        if key == 'seed':
            if not isinstance(config['seed'], int):
                config['seed'] = defaut.seed
        if key == 'level_max_time':
            if not isinstance(config['level_max_time'], int):
                config['level_max_time'] = defaut.level_max_time
        if key == 'highscore_filename':
            if not isinstance(config['highscore_filename'], str):
                config['highscore_filename'] = defaut.highscore_filename
        if key == 'levels':
            for _ in range(len(config['levels'])):
                if not isinstance(config['levels'][_]['id'], int):
                    config['levels'][_]['id'] = defaut.levels[_]['id']
                if not isinstance(config['levels'][_]['height'], int):
                    config['levels'][_]['height'] = defaut.levels[_]['height']
                if not isinstance(config['levels'][_]['width'], int):
                    config['levels'][_]['width'] = defaut.levels[_]['width']

    return config


# if __name__ == "__main__":
#     print((check_config(extract_dict("config.json"))))
