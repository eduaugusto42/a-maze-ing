PYTHON = python3
CONFIG = config.txt

.PHONY: help install run debug clean lint lint-strict test build

help:
	@echo "A-Maze-ing - available targets"
	@echo ""
	@echo "  make install       - install the development dependencies"
	@echo "  make run           - generate the maze (CONFIG=<file> to override)"
	@echo "  make debug         - run the program under pdb"
	@echo "  make clean         - remove caches and build artifacts"
	@echo "  make lint          - flake8 + mypy"
	@echo "  make lint-strict   - flake8 + mypy --strict"
	@echo "  make test          - run the test suite"
	@echo "  make build         - build the reusable mazegen package"

install:
	$(PYTHON) -m pip install "flake8>=7.0.0" "mypy>=1.10.0" "pytest>=8.0.0" \
		"build>=1.2.0" "setuptools>=68.0.0" "wheel>=0.42.0"

run:
	$(PYTHON) a_maze_ing.py $(CONFIG)

debug:
	$(PYTHON) -m pdb a_maze_ing.py $(CONFIG)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	rm -rf build dist ./*.egg-info .pdbhistory

lint:
	flake8 .
	mypy . --warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict

test:
	@if ls test_*.py >/dev/null 2>&1; then \
		$(PYTHON) -m pytest -v; \
	else \
		echo "No test_*.py file found: nothing to run."; \
	fi

build:
	@if [ ! -f pyproject.toml ]; then \
		echo "Error: pyproject.toml not found - it is needed to build the"; \
		echo "       mazegen package described in Chapter VI of the subject."; \
		exit 1; \
	fi
	$(PYTHON) -m build
	cp dist/mazegen-*.whl .
	cp dist/mazegen-*.tar.gz .
	@echo ""
	@echo "Package built, at the root of the repository:"
	@ls -1 mazegen-*
