PYTHON ?= python3
VENV ?= .venv
VENV_BIN := $(VENV)/bin
VENV_PY := $(VENV_BIN)/python
VENV_PIP := $(VENV_BIN)/pip
MAIN ?= a_maze_ing.py
REQ ?= requirements.txt
MYPY_FLAGS := --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
PACKAGE ?= mazegen
SRC = maze_animate.py maze_format.py maze_pathfinding.py maze_visualize.py a_maze_ing.py

.PHONY: run debug clean lint lint-strict

$(VENV_PY):
	$(PYTHON) -m venv $(VENV)
	$(VENV_PIP) install --upgrade pip
	@if [ -f $(REQ) ]; then \
		$(VENV_PIP) install -r $(REQ); \
	else \
		echo "No $(REQ) found; skipping dependency install"; \
	fi
	$(VENV_PIP) install --upgrade mazegen-1.0.0-py3-none-any.whl

install: $(VENV_PY)
	@echo "Environment ready."

run: install
	$(PYTHON) $(MAIN) config.txt -v

debug: install
	$(PYTHON) -m pdb $(MAIN) config.txt

clean:
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -prune -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -prune -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

lint: install
	$(VENV_BIN)/flake8 $(SRC)
	$(VENV_BIN)/mypy $(SRC) $(MYPY_FLAGS)

lint-strict: install
	$(VENV_BIN)/flake8 $(SRC)
	$(VENV_BIN)/mypy $(SRC) $(MYPY_FLAGS) --strict
