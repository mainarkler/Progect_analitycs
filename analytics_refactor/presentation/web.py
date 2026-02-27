"""Public web adapter for external users (FastAPI + Jinja2 templates)."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from analytics_refactor.application.container import build_container
from analytics_refactor.domain.errors import DomainError
from analytics_refactor.infrastructure.logging_setup import configure_logging
from analytics_refactor.schemas.dtos import SellStressRequest, VMCalculationRequest

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

container = build_container()
configure_logging(container.settings.log_level)

app = FastAPI(title="Analytics Refactor Web", version="0.1.0")
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "sell_stress_result": None,
            "vm_result": None,
            "error": None,
        },
    )


@app.post("/calculate", response_class=HTMLResponse)
def calculate(
    request: Request,
    notional: float = Form(...),
    shock_pct: float = Form(...),
    contracts: int = Form(...),
    price_open: float = Form(...),
    price_current: float = Form(...),
    lot_size: float = Form(...),
) -> HTMLResponse:
    try:
        sell_stress_result = container.sell_stress_service.calculate(
            SellStressRequest(notional=notional, shock_pct=shock_pct)
        )
        vm_result = container.vm_calculation_service.calculate(
            VMCalculationRequest(
                contracts=contracts,
                price_open=price_open,
                price_current=price_current,
                lot_size=lot_size,
            )
        )
        context = {
            "sell_stress_result": sell_stress_result.model_dump(),
            "vm_result": vm_result.model_dump(),
            "error": None,
        }
    except (DomainError, ValueError) as exc:
        context = {
            "sell_stress_result": None,
            "vm_result": None,
            "error": f"Input error: {exc}",
        }

    return templates.TemplateResponse(request=request, name="index.html", context=context)
