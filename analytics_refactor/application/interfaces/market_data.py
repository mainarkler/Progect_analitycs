"""Ports used by application services."""

from abc import ABC, abstractmethod

from analytics_refactor.schemas.dtos import InstrumentPriceDTO


class MarketDataProvider(ABC):
    """Read-only market data port."""

    @abstractmethod
    def get_last_price(self, ticker: str) -> InstrumentPriceDTO:
        """Return last known price for ticker."""
