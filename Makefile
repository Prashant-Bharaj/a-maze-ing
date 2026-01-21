PYTHON ?= python3
VENV ?= .venv
VENV_BIN := $(VENV)/bin
MAIN ?= a_maze_ing.py
REQ ?= requirements.txt
MYPY_FLAGS := --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
PACKAGE ?= mazegen

.PHONY: install run debug clean lint lint-strict package

install:
	$(PYTHON) -m venv $(VENV)
	$(VENV_BIN)/pip install --upgrade pip
	@if [ -f $(REQ) ]; then \
		$(VENV_BIN)/pip install -r $(REQ); \
	else \
		echo "No $(REQ) found; skipping dependency install"; \
	fi
	pip install --force-reinstall mazegen-1.0.0-py3-none-any.whl

run: install
	. $(VENV_BIN)/activate && $(PYTHON) $(MAIN) config.txt

debug: install
	. $(VENV_BIN)/activate && $(PYTHON) -m pdb $(MAIN) config.txt

clean:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -prune -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -prune -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

lint: install
	. $(VENV_BIN)/activate && $(VENV_BIN)/flake8 .
	. $(VENV_BIN)/activate && $(VENV_BIN)/mypy . $(MYPY_FLAGS)

lint-strict: install
	. $(VENV_BIN)/activate && $(VENV_BIN)/flake8 .
	. $(VENV_BIN)/activate && $(VENV_BIN)/mypy . --strict

package: install
	@echo "Building mazegen package..."
	. $(VENV_BIN)/activate && $(VENV_BIN)/pip install --upgrade build
	. $(VENV_BIN)/activate && $(PYTHON) -m build
	@echo "Copying wheel to repository root..."
	@cp dist/$(PACKAGE)-*.whl . 2>/dev/null || true
	@echo "Package built successfully! Files in dist/"
