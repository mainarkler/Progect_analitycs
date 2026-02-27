.PHONY: install run test lint

install:
	python -m pip install -r requirements.txt

run:
	PYTHONPATH=.. python -m analytics_refactor.presentation.cli

test:
	pytest -q

lint:
	ruff check analytics_refactor
