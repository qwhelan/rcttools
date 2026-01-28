from decimal import Decimal
from typing import Tuple

import pytest

from ..common import dec_to_dms


@pytest.mark.parametrize(
    "decimal_degrees, expected",
    [
        (Decimal("0.0"), (Decimal("0"), Decimal("0"), Decimal("0"))),
        (Decimal("1.5"), (Decimal("1"), Decimal("30"), Decimal("0"))),
        (Decimal("-1.5"), (Decimal("1"), Decimal("30"), Decimal("0"))),
        (Decimal("90"), (Decimal("90"), Decimal("0"), Decimal("0"))),
        (Decimal("47.62265"), (Decimal("47"), Decimal("37"), Decimal("21.54"))),
    ],
)
def test_dec_to_dms(
    decimal_degrees: Decimal, expected: Tuple[Decimal, Decimal, Decimal]
) -> None:
    result = dec_to_dms(decimal_degrees)
    assert result == expected
