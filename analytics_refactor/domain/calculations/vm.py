"""Variation margin (VM) simplified formulas for FORTS-style futures."""

from analytics_refactor.domain.errors import InvalidCalculationInputError


class VMCalculator:
    """Calculates simplified variation margin for educational/reference use."""

    @staticmethod
    def variation_margin(
        contracts: int,
        price_open: float,
        price_current: float,
        lot_size: float,
    ) -> float:
        """Compute variation margin.

        Formula: (price_current - price_open) * contracts * lot_size
        """
        if contracts == 0:
            return 0.0
        if lot_size <= 0:
            raise InvalidCalculationInputError("lot_size must be positive")
        if price_open < 0 or price_current < 0:
            raise InvalidCalculationInputError("prices must be non-negative")
        return (price_current - price_open) * contracts * lot_size
