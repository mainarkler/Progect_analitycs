# Analytics Refactor Scaffold

A clean-architecture Python 3.11+ scaffold for a financial analytics platform that can be attached to Streamlit, FastAPI, Django, or other adapters later.

## Goals

- Split responsibilities into layers.
- Keep domain logic framework-agnostic.
- Make external integrations replaceable.
- Improve testability and maintainability.

## Layering

- `presentation/` — adapter entry points (CLI today, Streamlit/FastAPI later)
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
    __init__.py
    presentation/
      __init__.py
      cli.py
    application/
      __init__.py
      container.py
      interfaces/
        __init__.py
        market_data.py
      services/
        __init__.py
        sell_stress_service.py
        vm_calculation_service.py
    domain/
      __init__.py
      errors.py
      calculations/
        __init__.py
        sell_stress.py
        vm.py
    infrastructure/
      __init__.py
      config.py
      errors.py
      logging_setup.py
      clients/
        __init__.py
        moex_client.py
    schemas/
      __init__.py
      dtos.py
    tests/
      __init__.py
      unit/
        __init__.py
        domain/
          __init__.py
          test_vm_calculator.py
```

## Error Handling Strategy

- `domain.errors` for business rule failures.
- `infrastructure.errors` for network/provider failures.
- Application layer orchestrates and can map errors to whichever adapter is used later.

## Dependency Injection

Manual DI in `application/container.py` wires services and infrastructure adapters in one place.

## Run

```bash
make install
make run
```

## Test

```bash
make test
```

## Migration Path

- **To Streamlit:** build `presentation/streamlit_app.py`, inject `build_container()`, call services from callbacks.
- **To FastAPI/Django:** create endpoint/controller adapters that validate input -> DTO -> service -> DTO -> response.
