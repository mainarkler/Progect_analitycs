"""Application service for VM calculations."""

from analytics_refactor.domain.calculations.vm import VMCalculator
from analytics_refactor.schemas.dtos import VMCalculationRequest, VMCalculationResult


class VMCalculationService:
    """Runs validation + domain formula for variation margin."""

    def calculate(self, request: VMCalculationRequest) -> VMCalculationResult:
        vm = VMCalculator.variation_margin(
            contracts=request.contracts,
            price_open=request.price_open,
            price_current=request.price_current,
            lot_size=request.lot_size,
        )
        return VMCalculationResult(variation_margin=vm)
