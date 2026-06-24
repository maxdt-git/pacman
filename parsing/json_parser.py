import json
from typing import Any
from parsing import DefaultConfig


def extract_config(jsonfile: str) -> Any | None:
    """
    Open the jsonfile where the highscores are saved and transforms
    the data so they can be used

    Arguments:
    jsonfile -- name of the config file
    """
    try:
        with open(jsonfile, "r") as file:
            return json.load(file)
    except Exception as e:
        print(e)
        return None


def check_config(config: dict[str, Any] | None) -> dict[str, Any] | None:
    """
    Parse the config, if a value is missing or wrongly set, set the value
    with a default value and returns either the config parsed or none

    Arguments:
    config -- value we extract from extract_config()
    """
    mandatory_keys = [
        "pacgum", "points_per_pacgum", "points_per_super_pacgum",
        "points_per_ghost", "seed", "level_max_time", "lives",
        "highscore_filename"]
    spec_keys = [
        "id", "width", "height", "pacgum"
    ]

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

    for spec in spec_keys:
        if len(config['levels']) != 10:
            config['levels'] = defaut.levels
            print("Not enough levels in the config file, set to defaut value")
        for _ in range(len(config['levels'])):
            if spec not in config['levels'][_]:
                default_level = defaut.levels[_] if _ < len(defaut.levels) \
                    else defaut.levels[0]
                if spec == 'id':
                    config['levels'][_]['id'] = default_level['id']
                if spec == 'height':
                    config['levels'][_]['height'] = default_level['height']
                if spec == 'width':
                    config['levels'][_]['width'] = default_level['width']
                if spec == 'pacgum':
                    config['levels'][_]['pacgum'] = default_level['pacgum']

                print(f"{spec} missing in level {_}, set to default value "
                      f"{config['levels'][_][spec]}")

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
            for _ in range(len(config[key])):
                if not isinstance(config[key][_]['id'], int):
                    config[key][_]['id'] = defaut.levels[_]['id']
                if not isinstance(config[key][_]['height'], int):
                    config[key][_]['height'] = defaut.levels[_]['height']
                if not isinstance(config[key][_]['width'], int):
                    config[key][_]['width'] = defaut.levels[_]['width']
                if not isinstance(config[key][_]['pacgum'], int):
                    config[key][_]['Pacgum'] = defaut.levels[_]['pacgum']
                if config['pacgum'] > config[key][_]['height'] * \
                        config[key][_]['width'] - 22:
                    config['pacgum'] = defaut.pacgum

    return config
