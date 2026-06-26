CONFIG = config.json
MAIN = pac-man.py

venv:
	python3 -m venv pacman_venv

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

package:
	pacman_venv/bin/pyinstaller pac-man.py --add-data "assets:assets" --add-data "fonts:fonts" --add-data "config.json:."

del-pack:
	rm -rf dist build pac-man.spec

zip:
	cd dist
	zip -r ../pac-man-linux.zip pac-man/

.PHONY: venv install run debug clean lint lint-strict del-pack zip
