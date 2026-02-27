"""Framework-agnostic entrypoint.

Can be replaced later with Streamlit/FastAPI adapters while reusing services.
"""

from analytics_refactor.application.container import build_container
from analytics_refactor.infrastructure.logging_setup import configure_logging
from analytics_refactor.schemas.dtos import SellStressRequest, VMCalculationRequest


def main() -> None:
    container = build_container()
    configure_logging(container.settings.log_level)

    sell_stress_result = container.sell_stress_service.calculate(
        SellStressRequest(notional=1_000_000, shock_pct=0.12)
    )
    vm_result = container.vm_calculation_service.calculate(
        VMCalculationRequest(contracts=5, price_open=101.2, price_current=99.8, lot_size=10)
    )

    print(f"Sell Stress: {sell_stress_result.model_dump()}")
    print(f"Variation Margin: {vm_result.model_dump()}")


if __name__ == "__main__":
    main()
