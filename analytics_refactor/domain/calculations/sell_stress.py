"""Sell stress domain formulas."""

from analytics_refactor.domain.errors import InvalidCalculationInputError


class SellStressCalculator:
    """Encapsulates stress-loss calculations for instrument portfolios."""

    @staticmethod
    def stressed_value(notional: float, shock_pct: float) -> float:
        """Return position value after a stress shock.

        shock_pct example: 0.10 => -10% price shock.
        """
        if notional < 0:
            raise InvalidCalculationInputError("notional must be non-negative")
        if shock_pct < 0 or shock_pct > 1:
            raise InvalidCalculationInputError("shock_pct must be between 0 and 1")
        return notional * (1 - shock_pct)

    @staticmethod
    def stress_loss(notional: float, shock_pct: float) -> float:
        """Return absolute loss under stress scenario."""
        stressed = SellStressCalculator.stressed_value(notional=notional, shock_pct=shock_pct)
        return notional - stressed
