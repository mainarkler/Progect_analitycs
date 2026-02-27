from analytics_refactor.domain.calculations.vm import VMCalculator


def test_variation_margin_formula() -> None:
    # (105 - 100) * 3 * 10 = 150
    result = VMCalculator.variation_margin(
        contracts=3,
        price_open=100.0,
        price_current=105.0,
        lot_size=10.0,
    )
    assert result == 150.0
