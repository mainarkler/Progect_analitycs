"""Application service orchestrating sell stress use cases."""

from analytics_refactor.domain.calculations.sell_stress import SellStressCalculator
from analytics_refactor.schemas.dtos import SellStressRequest, SellStressResult


class SellStressService:
    """Coordinates validation DTOs and domain calculations."""

    def calculate(self, request: SellStressRequest) -> SellStressResult:
        stressed_value = SellStressCalculator.stressed_value(
            notional=request.notional,
            shock_pct=request.shock_pct,
        )
        stress_loss = SellStressCalculator.stress_loss(
            notional=request.notional,
            shock_pct=request.shock_pct,
        )
        return SellStressResult(stressed_value=stressed_value, stress_loss=stress_loss)
