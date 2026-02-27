from analytics_refactor.domain.calculations.sell_stress import SellStressCalculator


def test_stress_loss_formula() -> None:
    # 1_000_000 with 12% shock => 120_000 loss
    result = SellStressCalculator.stress_loss(notional=1_000_000, shock_pct=0.12)
    assert result == 120_000
