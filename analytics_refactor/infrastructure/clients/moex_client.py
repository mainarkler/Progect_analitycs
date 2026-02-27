"""MOEX API client adapter with simple retry/backoff."""

from __future__ import annotations

import logging
import time

import requests

from analytics_refactor.application.interfaces.market_data import MarketDataProvider
from analytics_refactor.infrastructure.errors import ExternalAPIError
from analytics_refactor.schemas.dtos import InstrumentPriceDTO

logger = logging.getLogger(__name__)


class MOEXClient(MarketDataProvider):
    """HTTP adapter for MOEX ISS endpoints."""

    def __init__(self, base_url: str, timeout: float, retries: int, backoff_seconds: float) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._retries = retries
        self._backoff = backoff_seconds

    def get_last_price(self, ticker: str) -> InstrumentPriceDTO:
        endpoint = f"{self._base_url}/iss/engines/stock/markets/shares/securities/{ticker}.json"
        for attempt in range(1, self._retries + 1):
            try:
                response = requests.get(endpoint, timeout=self._timeout)
                response.raise_for_status()
                payload = response.json()

                # Simplified extraction for scaffold purposes.
                marketdata = payload.get("marketdata", {}).get("data", [])
                columns = payload.get("marketdata", {}).get("columns", [])
                last_price_idx = columns.index("LAST") if "LAST" in columns else None
                if not marketdata or last_price_idx is None:
                    raise ExternalAPIError("MOEX response missing market data")

                raw_price = marketdata[0][last_price_idx]
                if raw_price is None:
                    raise ExternalAPIError(f"Ticker {ticker} has no LAST price")

                return InstrumentPriceDTO(ticker=ticker, last_price=float(raw_price))
            except (requests.RequestException, ValueError, ExternalAPIError) as exc:
                logger.warning("MOEX request failed (attempt %s/%s): %s", attempt, self._retries, exc)
                if attempt == self._retries:
                    raise ExternalAPIError(f"Failed to fetch MOEX data for {ticker}") from exc
                time.sleep(self._backoff * attempt)

        raise ExternalAPIError(f"Unexpected retry flow for ticker {ticker}")
