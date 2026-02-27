.PHONY: install run run-web test lint

install:
	python -m pip install -r requirements.txt

run:
	PYTHONPATH=.. python -m analytics_refactor.presentation.cli

run-web:
	PYTHONPATH=.. uvicorn analytics_refactor.presentation.web:app --host 0.0.0.0 --port 8000

test:
	pytest -q

lint:
	ruff check analytics_refactor
