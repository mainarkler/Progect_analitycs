# Analytics Refactor Scaffold

A clean-architecture Python 3.11+ scaffold for a financial analytics platform that can be attached to Streamlit, FastAPI, Django, or other adapters later.

## Goals

- Split responsibilities into layers.
- Keep domain logic framework-agnostic.
- Make external integrations replaceable.
- Improve testability and maintainability.

## Layering

- `presentation/` — adapter entry points (CLI and web app)
- `application/` — use-case orchestration and dependency wiring
- `domain/` — pure business formulas and domain errors
- `infrastructure/` — HTTP clients, runtime config, logging
- `schemas/` — Pydantic DTOs for I/O contracts
- `tests/` — unit tests for domain/application behavior

## Project Structure

```text
analytics_refactor/
  .env.template
  Makefile
  README.md
  pyproject.toml
  requirements.txt
  analytics_refactor/
    presentation/
      cli.py
      web.py
      templates/
        index.html
      static/
        styles.css
    application/
      container.py
      interfaces/
        market_data.py
      services/
        sell_stress_service.py
        vm_calculation_service.py
    domain/
      errors.py
      calculations/
        sell_stress.py
        vm.py
    infrastructure/
      config.py
      errors.py
      logging_setup.py
      clients/
        moex_client.py
    schemas/
      dtos.py
    tests/
      unit/
        domain/
          test_vm_calculator.py
```

## Quick Start For External Users

```bash
git clone <your-repo-url>
cd Progect_analitycs/analytics_refactor
python3.11 -m venv .venv
source .venv/bin/activate
make install
```

### CLI demo

```bash
make run
```

### Public web app (FastAPI)

```bash
make run-web
```

Open in browser: <http://localhost:8000>

## Configuration

Copy `.env.template` to `.env` and adjust values:

- API hosts (`MOEX_BASE_URL`, `CBR_BASE_URL`)
- HTTP timeout/retry controls
- app environment and log level

## Error Handling Strategy

- `domain.errors` for business rule failures.
- `infrastructure.errors` for network/provider failures.
- Presentation layer maps errors to user-facing responses.

## Dependency Injection

Manual DI in `application/container.py` wires services and infrastructure adapters in one place.

## Test

```bash
make test
```

## Migration Path

- **To Streamlit:** build `presentation/streamlit_app.py`, inject `build_container()`, call services from callbacks.
- **To FastAPI/Django:** current `presentation/web.py` is already a FastAPI adapter; you can split routes further by domain.
