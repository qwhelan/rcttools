from decimal import Decimal
from typing import Tuple

import pytest

from ..common import calc_bearing, dec_to_dms


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


@pytest.mark.parametrize(
    "lat1, lon1, lat2, lon2, expected_bearing",
    [
        (Decimal("0"), Decimal("0"), Decimal("1"), Decimal("0"), Decimal("0.000000")),
        (Decimal("0"), Decimal("0"), Decimal("0"), Decimal("1"), Decimal("90.000000")),
        (
            Decimal("0"),
            Decimal("0"),
            Decimal("0.1"),
            Decimal("0.1"),
            Decimal("44.999956"),
        ),
        (
            Decimal("0"),
            Decimal("0"),
            Decimal("-1"),
            Decimal("0"),
            Decimal("180.000000"),
        ),
        (Decimal("0"), Decimal("0"), Decimal("0"), Decimal("0"), None),
    ],
)
def test_calc_bearing(
    lat1: Decimal,
    lon1: Decimal,
    lat2: Decimal,
    lon2: Decimal,
    expected_bearing: Decimal,
) -> None:
    result = calc_bearing(lat1, lon1, lat2, lon2)
    assert result == expected_bearing
