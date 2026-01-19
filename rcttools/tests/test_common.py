from decimal import Decimal
from typing import Tuple

import pytest

from ..common import dec_to_dms


@pytest.mark.parametrize(
    "decimal_degrees, expected",
    [
        (0.0, (0, 0, 0)),
        (1.5, (1, 30, 0)),
        (-1.5, (1, 30, 0)),
        (90, (90, 0, 0)),
    ],
)
def test_dec_to_dms(
    decimal_degrees: Decimal, expected: Tuple[Decimal, Decimal, Decimal]
) -> None:
    result = dec_to_dms(decimal_degrees)
    assert result == expected
