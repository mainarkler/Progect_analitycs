# Analytics Refactor Scaffold

A clean-architecture Python 3.11+ scaffold for a financial analytics platform that can be attached to Streamlit, FastAPI, Django, or other adapters later.

## What is ready for external users

- Browser UI at `/` for manual calculations.
- Public JSON API at `/api/v1/calculate`.
- Health endpoint at `/health`.
- Local run, Docker run, and production deployment templates (systemd + Nginx).

## Layering

- `presentation/` — adapter entry points (CLI + FastAPI web)
- `application/` — use-case orchestration and dependency wiring
- `domain/` — pure business formulas and domain errors
- `infrastructure/` — HTTP clients, runtime config, logging
- `schemas/` — Pydantic DTOs for I/O contracts
- `tests/` — unit tests for domain/application behavior

## Quick Start (external users)

```bash
git clone <your-repo-url>
cd Progect_analitycs/analytics_refactor
make bootstrap
source .venv/bin/activate
make run-web
```

Open in browser: <http://localhost:8000>

## API usage example

```bash
curl -X POST http://localhost:8000/api/v1/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "notional": 1000000,
    "shock_pct": 0.12,
    "contracts": 5,
    "price_open": 101.2,
    "price_current": 99.8,
    "lot_size": 10
  }'
```

## Configuration

Copy `.env.template` to `.env` and adjust values:

- API hosts (`MOEX_BASE_URL`, `CBR_BASE_URL`)
- HTTP timeout/retry controls
- app environment and log level

## Make targets

- `make bootstrap` — create venv, install deps, prepare `.env`.
- `make run` — CLI demo.
- `make run-web` — local web app with auto-reload.
- `make run-prod` — production-like web app run.
- `make test` — run unit tests.
- `make docker-up` / `make docker-down` — containerized run.

## Docker

```bash
cp .env.template .env
docker compose up --build -d
```

## Deploy on Linux VM (template)

1. Copy project to `/opt/analytics_refactor`.
2. Run bootstrap and ensure `.venv` + `.env` exist.
3. Install `deploy/systemd/analytics-refactor.service` to `/etc/systemd/system/`.
4. Enable and start service:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable analytics-refactor
   sudo systemctl start analytics-refactor
   ```
5. Configure Nginx using `deploy/nginx/analytics-refactor.conf` and add TLS (Let's Encrypt).

## Error handling strategy

- `domain.errors` for business rule failures.
- `infrastructure.errors` for network/provider failures.
- Presentation layer maps errors to user-facing messages and API responses.

## Migration path

- **To Streamlit:** create `presentation/streamlit_app.py`, inject `build_container()`, call services.
- **To FastAPI/Django:** this repo already includes FastAPI adapter; split routes by domain when needed.
