"""Manual dependency injection container."""

from dataclasses import dataclass

from analytics_refactor.application.services.sell_stress_service import SellStressService
from analytics_refactor.application.services.vm_calculation_service import VMCalculationService
from analytics_refactor.infrastructure.clients.moex_client import MOEXClient
from analytics_refactor.infrastructure.config import Settings


@dataclass(frozen=True)
class Container:
    settings: Settings
    sell_stress_service: SellStressService
    vm_calculation_service: VMCalculationService
    moex_client: MOEXClient


def build_container() -> Container:
    settings = Settings()
    return Container(
        settings=settings,
        sell_stress_service=SellStressService(),
        vm_calculation_service=VMCalculationService(),
        moex_client=MOEXClient(
            base_url=settings.moex_base_url,
            timeout=settings.http_timeout_seconds,
            retries=settings.http_retry_count,
            backoff_seconds=settings.http_retry_backoff_seconds,
        ),
    )
