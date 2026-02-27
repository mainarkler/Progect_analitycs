.PHONY: bootstrap install run run-web run-prod test lint docker-up docker-down

bootstrap:
	./scripts/bootstrap.sh

install:
	python -m pip install -r requirements.txt

run:
	PYTHONPATH=.. python -m analytics_refactor.presentation.cli

run-web:
	PYTHONPATH=.. uvicorn analytics_refactor.presentation.web:app --host 0.0.0.0 --port 8000 --reload

run-prod:
	PYTHONPATH=.. uvicorn analytics_refactor.presentation.web:app --host 0.0.0.0 --port 8000

test:
	pytest -q

lint:
	ruff check analytics_refactor

docker-up:
	docker compose up --build -d

docker-down:
	docker compose down
