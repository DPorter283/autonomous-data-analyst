.PHONY: install test lint format run

install:
	pip install -e .[dev]

test:
	pytest tests/

lint:
	ruff check src/

format:
	black src/

run:
	python src/main.py
