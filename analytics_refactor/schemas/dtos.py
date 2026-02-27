"""Transport DTOs and validation schemas (Pydantic)."""

from pydantic import BaseModel, Field, PositiveFloat


class SellStressRequest(BaseModel):
    notional: PositiveFloat = Field(..., description="Position size in currency")
    shock_pct: float = Field(..., ge=0.0, le=1.0, description="Stress shock in decimals")


class SellStressResult(BaseModel):
    stressed_value: float
    stress_loss: float


class VMCalculationRequest(BaseModel):
    contracts: int = Field(..., description="Number of futures contracts")
    price_open: float = Field(..., ge=0)
    price_current: float = Field(..., ge=0)
    lot_size: PositiveFloat


class VMCalculationResult(BaseModel):
    variation_margin: float


class InstrumentPriceDTO(BaseModel):
    ticker: str
    last_price: PositiveFloat
