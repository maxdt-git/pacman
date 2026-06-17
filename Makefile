CONFIG = config.json
MAIN = pac-man.py

venv:
	python3 -m venv pacman_venv

src:
	source pacman_venv/bin/activate

install: venv
	pacman_venv/bin/pip install mazegenerator-00001-py3-none-any.whl
	pacman_venv/bin/pip install -r requirements.txt 

run:
	pacman_venv/bin/python3 $(MAIN) $(CONFIG)

debug:
	pacman_venv/bin/python3 -m pdb $(MAIN) $(CONFIG)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +

lint:
	pacman_venv/bin/flake8 . --exclude=pacman_venv
	pacman_venv/bin/mypy . --warn-return-any --warn-unused-ignores \
	--ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	pacman_venv/bin/flake8 . --exclude=pacman_venv
	pacman_venv/bin/mypy --strict .

.PHONY: venv install run debug clean lint lint-strict