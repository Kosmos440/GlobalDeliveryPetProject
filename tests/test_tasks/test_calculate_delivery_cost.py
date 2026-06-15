from decimal import Decimal

from app.tasks.calculate_delivery_cost import _calculate_delivery_cost


def test_calculate_delivery_cost_formula():
    # weight=0.3, value_usd=1200, rate=100 → (0.15 + 12) * 100 = 1215.00
    cost = _calculate_delivery_cost(
        Decimal("0.3"),
        Decimal("1200"),
        Decimal("100"),
    )
    assert cost == Decimal("1215.00")
