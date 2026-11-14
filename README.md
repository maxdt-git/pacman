# Pac-Man

**Stack:** Python · Pygame · PyInstaller

**Highlights**
- Full game: 10 levels, procedurally generated mazes, highscores, menus, pause and tutorial screens
- Ghost AI switching between chase, flee and wander behaviours
- Packaged as a standalone executable with PyInstaller

## Description

A complete recreation of the classic Pac-Man arcade game built in Python with Pygame. Navigate through procedurally generated mazes, eat pacgums, avoid (or hunt) ghosts, and beat your highscore across 10 levels of increasing difficulty.

## Instructions

### Requirements

- Python 3.10+
- The `mazegenerator` package (provided as `.whl`)

### Installation

```bash
make install
```

This creates a virtual environment and installs all dependencies.

### Run

```bash
make run
# or directly:
python3 pac-man.py config.json
```

The program takes exactly one argument: a JSON configuration file.

### Other Makefile targets

| Target | Description |
|--------|-------------|
| `make debug` | Run with Python's built-in debugger (pdb) |
| `make lint` | Run flake8 + mypy |
| `make clean` | Remove `__pycache__` and `.mypy_cache` |
| `make package` | create a new game package |
| `make del-pack` | Remove all the file created with make package |
| `make zip` | zip the package so we can import it |

## Controls

| Key | Action |
|-----|--------|
| Arrow keys / WASD | Move Pac-Man |
| ESC | Pause / unpause |
| C | Toggle cheat mode |
| L | Skip to next level (cheat) |

### Cheat mode

Press **C** during gameplay to toggle cheat mode: Pac-Man becomes invincible and can walk through walls freely. Press **C** again to disable it. Press **L** to skip the current level.

## Configuration

The config file is a standard JSON file. Lines starting with `#` are treated as comments and ignored. All keys are optional — missing or invalid values are replaced by defaults with a warning message (no crash).

```json
{
    "highscore_filename": "highscore.json",
    "lives": 3,
    "seed": 42,
    "level_max_time": 90,
    "points_per_pacgum": 10,
    "points_per_super_pacgum": 50,
    "points_per_ghost": 200,
    "levels": [
        { "id": 1, "width": 15, "height": 15, "pacgum": 10 },
        ...
    ]
}
```

| Key | Default | Description |
|-----|---------|-------------|
| `highscore_filename` | `"highscore.json"` | Path to the highscore file |
| `lives` | `3` | Starting number of lives |
| `seed` | `42` | Seed used for the first level's maze |
| `level_max_time` | `90` | Time limit per level (seconds) |
| `points_per_pacgum` | `10` | Points for eating a pacgum |
| `points_per_super_pacgum` | `50` | Points for eating a super-pacgum |
| `points_per_ghost` | `200` | Points for eating a vulnerable ghost |
| `levels` | 10 default levels | Array of 10 level descriptors (id, width, height, pacgum count) |

The config must define exactly 10 levels. If fewer are provided, defaults are used.

## Highscore

Highscores are stored in a JSON file at the path defined by `highscore_filename` in the config (default: `highscore.json`, saved in the project directory).

At game end (win or lose), the player is prompted to enter their name (max 10 alphanumeric characters). The top 10 scores are kept, sorted by score descending. The file is loaded at startup and saved after each game session. If the file is missing or corrupted, it is silently reset to an empty state.

This approach was chosen for its simplicity and human-readability — the file can be inspected or reset manually without tooling.

## Maze Generation

Mazes are generated using the externally assigned `mazegenerator` package (installed from the provided `.whl`). The package is used as-is, without modification.

- Level 1 uses a fixed seed (`seed` from config, default `42`) for a reproducible starting maze.
- Subsequent levels use a random seed (`0`) for variety.
- The `PERFECT` parameter is set to `False` to produce Pac-Man-compatible corridors with multiple paths.
- If the generator raises an exception, the error is caught and reported cleanly.

The grid module (`grid/grid.py`) converts the generator's output into Pygame `Rect` objects for rendering.

## Implementation

The game runs at 60 FPS using `pygame.Clock`. Movement is grid-based (cell-to-cell), not pixel-based. Ghosts move every 500ms via a timer. Ghost AI switches between three behaviors:

- **Chase**: picks the adjacent cell that minimizes Manhattan distance to Pac-Man (when close and ghosts are normal).
- **Flee**: picks the adjacent cell that maximizes Manhattan distance (when Pac-Man has power-up active).
- **Wander**: random corridor traversal (when far from player).

Power-up lasts 5 seconds. Dead ghosts respawn at their corner after 2.5 seconds.

## General Software Architecture

```
pac-man.py          — entry point, main game loop, state machine
generator.py        — Game, Pac, Ghosts, Gum, MegaGum classes
parsing/
  json_parser.py    — extract_config(), check_config() with defaults
  class_parser.py   — Config and DefaultConfig dataclasses
  __init__.py
grid/
  grid.py           — maze rendering (draw_all, open_cells)
  __init__.py
screens/
  menu.py           — main menu
  score.py          — highscore screen
  tuto.py           — instructions screen
  pause.py          — pause overlay
  game_over.py      — game over + name entry
  victory.py        — victory + name entry
  __init__.py
assets/             — sprites (pacman, ghosts, power-up)
fonts/              — Pixeltype.ttf
config.json         — default configuration
highscore.json      — persistent highscore file (auto-created)
```

The main loop is a state machine with states: `menu`, `game`, `pause`, `score`, `tuto`, `over`, `victory`. Each state delegates input and rendering to the corresponding module.

## Project Management

Project management documents task tracking, team organization are available in the [`project_management/`](project_management/) directory.

## Resources

- [Pygame documentation](https://www.pygame.org/docs/)
- [Original Pac-Man ghost AI](https://www.gamedeveloper.com/design/the-pac-man-dossier)

**AI usage:** Claude Code was used to help write this README. Game logic, architecture, and all Python code were written by the team. AI was not used to generate functional code. All AI-assisted content was reviewed and validated by both team members.
