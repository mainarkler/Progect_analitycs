"""Public web adapter for external users (FastAPI + Jinja2 templates)."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from analytics_refactor.application.container import build_container
from analytics_refactor.domain.errors import DomainError
from analytics_refactor.infrastructure.logging_setup import configure_logging
from analytics_refactor.schemas.dtos import SellStressRequest, VMCalculationRequest

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

container = build_container()
configure_logging(container.settings.log_level)

app = FastAPI(title="Analytics Refactor Web", version="0.2.0")
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


class CalculationPayload(BaseModel):
    notional: float = Field(..., gt=0)
    shock_pct: float = Field(..., ge=0, le=1)
    contracts: int
    price_open: float = Field(..., ge=0)
    price_current: float = Field(..., ge=0)
    lot_size: float = Field(..., gt=0)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "analytics-refactor"}


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


def _run_calculations(payload: CalculationPayload) -> dict[str, dict[str, float]]:
    sell_stress_result = container.sell_stress_service.calculate(
        SellStressRequest(notional=payload.notional, shock_pct=payload.shock_pct)
    )
    vm_result = container.vm_calculation_service.calculate(
        VMCalculationRequest(
            contracts=payload.contracts,
            price_open=payload.price_open,
            price_current=payload.price_current,
            lot_size=payload.lot_size,
        )
    )
    return {
        "sell_stress": sell_stress_result.model_dump(),
        "variation_margin": vm_result.model_dump(),
    }


@app.post("/api/v1/calculate")
def calculate_api(payload: CalculationPayload) -> dict[str, object]:
    try:
        return {"ok": True, "data": _run_calculations(payload)}
    except (DomainError, ValueError) as exc:
        return {"ok": False, "error": str(exc)}


@app.post("/calculate", response_class=HTMLResponse)
def calculate_form(
    request: Request,
    notional: float = Form(...),
    shock_pct: float = Form(...),
    contracts: int = Form(...),
    price_open: float = Form(...),
    price_current: float = Form(...),
    lot_size: float = Form(...),
) -> HTMLResponse:
    try:
        payload = CalculationPayload(
            notional=notional,
            shock_pct=shock_pct,
            contracts=contracts,
            price_open=price_open,
            price_current=price_current,
            lot_size=lot_size,
        )
        results = _run_calculations(payload)
        context = {
            "sell_stress_result": results["sell_stress"],
            "vm_result": results["variation_margin"],
            "error": None,
        }
    except (DomainError, ValueError) as exc:
        context = {
            "sell_stress_result": None,
            "vm_result": None,
            "error": f"Input error: {exc}",
        }

    return templates.TemplateResponse(request=request, name="index.html", context=context)
